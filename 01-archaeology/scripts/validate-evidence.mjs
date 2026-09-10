import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const repository = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const archaeology = path.join(repository, '01-archaeology');
const library = path.join(archaeology, 'legacy-sifap/natural-programs');
const adabas = path.join(archaeology, 'legacy-sifap/adabas-ddms');
const artifacts = [
    'inventory.md', 'business-rules-catalog.md', 'dependency-map.md', 'data-map.md',
    'program-data-dictionary.md', 'reading-coverage.md', 'mysteries-found.md',
    'glossary.md', 'discovery-report.md', 'LEGACY-EXPLORATION-CHECKLIST.md',
];

export function controlBlocks(source) {
    const stacks = { IF: [], DECIDE: [], REPORT: [], ERROR: [] };
    const blocks = { IF: [], DECIDE: [], REPORT: [], ERROR: [] };
    source.split(/\r?\n/).forEach((raw, index) => {
        const line = raw.trim();
        if (line.startsWith('*')) return;
        let kind;
        let ending;
        if (/^IF\b/.test(line)) kind = 'IF';
        else if (/^DECIDE\b/.test(line)) kind = 'DECIDE';
        else if (/^AT (BREAK|END OF DATA|START OF DATA|TOP OF PAGE)\b/.test(line)) kind = 'REPORT';
        else if (/^ON ERROR\b/.test(line)) kind = 'ERROR';
        if (kind) stacks[kind].push(index + 1);
        if (/^END-(IF|NOREC)\b/.test(line)) ending = 'IF';
        else if (/^END-DECIDE\b/.test(line)) ending = 'DECIDE';
        else if (/^END-(BREAK|ENDDATA|START|TOPPAGE)\b/.test(line)) ending = 'REPORT';
        else if (/^END-ERROR\b/.test(line)) ending = 'ERROR';
        if (ending) {
            const start = stacks[ending].pop();
            assert.ok(start, `Unpaired ${line} at line ${index + 1}`);
            blocks[ending].push(`${start}-${index + 1}`);
        }
    });
    for (const [kind, stack] of Object.entries(stacks)) {
        assert.equal(stack.length, 0, `Unclosed ${kind}: ${stack.join(', ')}`);
        blocks[kind].sort((left, right) => Number(left.split('-')[0]) - Number(right.split('-')[0]));
    }
    return blocks;
}

export function declaredVariables(source) {
    const declaration = source.split(/^END-DEFINE\s*$/m)[0];
    return Object.fromEntries([...declaration.matchAll(/^[ \t]*\d+[ \t]+(#[\w-]+)[ \t]+\(([^)\r\n]+)\)/gm)]
        .map(match => [match[1], match[2].replaceAll(' ', '')]));
}

function documentedVariables(section) {
    const variables = {};
    for (const line of section.split('\n')) {
        const typed = line.match(/^((?:[ANP]\d+(?:\.\d+)?|L)(?:\/[\d:,]+)?):/);
        const table = line.match(/^\| (#[^|]+) \| ((?:[ANP]\d+(?:\.\d+)?|L)(?:\/[\d:,]+)?) \|/);
        if (!typed && !table) continue;
        const names = typed ? line.slice(typed[0].length) : table[1];
        const format = typed ? typed[1] : table[2];
        for (const name of names.match(/#[\w-]+/g) ?? []) variables[name] = format;
    }
    return variables;
}

function section(document, heading) {
    const body = document.split(`### ${heading}\n`)[1];
    assert.ok(body !== undefined, `Missing dictionary section: ${heading}`);
    return body.split(/^#{1,3} /m)[0];
}

function cells(line) {
    return line.split('|').slice(1, -1).map(cell => cell.trim());
}

function questionRows(document, heading) {
    const body = document.split(`## ${heading}\n`)[1];
    assert.ok(body !== undefined, `Missing H1 section: ${heading}`);
    return body.split('\n## ')[0].split('\n')
        .filter(line => /^\| BONUS-Q\d{2} \|/.test(line)).map(cells);
}

function validateDispositions(document) {
    const questions = questionRows(document, 'Question register');
    const dispositions = questionRows(document, 'H1 dispositions');
    const expected = Array.from({ length: 41 }, (_, index) => `BONUS-Q${String(index + 1).padStart(2, '0')}`);
    assert.deepEqual(questions.map(row => row[0]), expected, 'H1 source-question IDs');
    assert.deepEqual(dispositions.map(row => row[0]), expected, 'H1 disposition IDs');
    for (const question of questions) {
        assert.equal(question[6], 'Awaiting human validation', `H1 source-question status: ${question[0]}`);
    }
    for (const row of dispositions) {
        const [identifier, disposition, action, owner, gate] = row;
        assert.equal(row.length, 5, `H1 disposition columns: ${identifier}`);
        assert.equal(disposition, identifier === 'BONUS-Q01' ? 'Scoped decision' : 'Deferred', `H1 disposition type: ${identifier}`);
        assert.ok(action.length > 0, `H1 action: ${identifier}`);
        assert.match(owner, /^Pair [1345] \/ [A-Za-z][A-Za-z ]+$/, `H1 owner: ${identifier}`);
        assert.ok(gate.startsWith('Before '), `H1 reopening gate: ${identifier}`);
    }
    return {
        dispositions: dispositions.length,
        scoped_decisions: dispositions.filter(row => row[1] === 'Scoped decision').length,
        deferred_questions: dispositions.filter(row => row[1] === 'Deferred').length,
    };
}

function checksum(file) {
    return createHash('sha256').update(readFileSync(file)).digest('hex');
}

function validateControlCoverage(source, name, controlTable, totals) {
    const blocks = controlBlocks(source);
    const row = controlTable.split('\n').find(line => line.startsWith(`| [${name}]`));
    assert.ok(row, `Missing control row: ${name}`);
    const columns = cells(row);
    for (const [kind, intervals] of Object.entries(blocks)) {
        const pattern = kind === 'REPORT' ? /AT (?:BREAK|END|START|TOP) (\d+-\d+)/g : /ON ERROR (\d+-\d+)/g;
        let documented;
        if (kind === 'IF' || kind === 'DECIDE') {
            const column = kind === 'IF' ? 1 : 2;
            documented = columns[column].match(/\b\d{1,6}-\d{1,6}\b/g) ?? [];
        } else {
            documented = [...columns[3].matchAll(pattern)].map(match => match[1]);
        }
        assert.deepEqual(documented, intervals, `${name}: ${kind} intervals`);
        totals[kind] += intervals.length;
    }
}

function validateDeclarationCoverage(source, name, dictionary, totals) {
    const member = name.split('.')[0];
    const auditMembers = new Set(['BATCHPGT', 'BATCHCON', 'CADBENEF', 'CADDEPEN', 'CADPROG', 'CALCCORR', 'CONSBENF']);
    const inlineMembers = new Set(['CADBENEF', 'VALBENEF', 'VALDOCS']);
    const sharedMembers = new Set(['CADDEPEN', 'SUBVALCP']);
    const heading = ['SUBVALCP', 'SUBVALNI'].includes(member) ? 'SUBVALCP.NSN and SUBVALNI.NSN' : name;
    let text = section(dictionary, heading);
    if (member === 'SUBVALCP') text = '';
    if (auditMembers.has(member)) text += section(dictionary, 'Audit work fields');
    if (inlineMembers.has(member)) text += section(dictionary, 'Inline CPF arithmetic fields');
    if (sharedMembers.has(member)) text += section(dictionary, 'Shared CPF work fields');
    const actual = declaredVariables(source);
    assert.deepEqual(documentedVariables(text), actual, `${name}: declared variable names/formats`);
    totals.variables += Object.keys(actual).length;
}

function validateMember(name, documents, totals) {
    const source = readFileSync(path.join(library, name), 'utf8');
    assert.ok(documents['reading-coverage.md'].includes(`[${name}]`), `Missing reading: ${name}`);
    const active = source.split('\n').filter(line => !line.trim().startsWith('*')).join('\n');
    for (const kind of ['CALLNAT', 'INCLUDE']) {
        totals[kind] += [...active.matchAll(new RegExp(String.raw`^[ \t]*${kind}\b`, 'gm'))].length;
    }
    totals.USING += active.split('\n').filter(line => /^(?:LOCAL|PARAMETER) USING\b/.test(line.trim())).length;
    if (/\.(NSP|NSN|NSC)$/.test(name)) {
        const controlTable = documents['reading-coverage.md'].split('## Control-block intervals\n')[1].split('\n## ')[0];
        validateControlCoverage(source, name, controlTable, totals);
    }
    if (/\.(NSP|NSN|NSA|NSL)$/.test(name)) {
        validateDeclarationCoverage(source, name, documents['program-data-dictionary.md'], totals);
    }
}

function validateDataFields(name, dataMap, totals) {
    const source = readFileSync(path.join(adabas, name), 'utf8');
    const tokens = source.split('\n').map(line => line.trim().split(/\s+/));
    const fieldRows = tokens.map(row => row[0] === 'M' ? row.slice(1) : row)
        .filter(row => /^[12]$/.test(row[0]) && /^[ANP]$/.test(row[3]));
    const fields = Object.fromEntries(fieldRows.map(row => [row[1], { name: row[2], format: row[3] + row[4].replace(',', '.') }]));
    const groups = tokens.filter(row => /^[GP]$/.test(row[0]) && /^[12]$/.test(row[1]));
    const derived = tokens.filter(row => row[0] === 'S' && /^[A-Z][A-Z0-9]$/.test(row[1]));
    const table = dataMap.split(`## ${name.split('.')[0]} fields\n`)[1].split('\n## ')[0];
    const rows = table.split('\n').filter(line => /^\| [A-Z][A-Z0-9] \| [A-Z][A-Z0-9-]+ \|/.test(line)).map(cells);
    assert.equal(rows.length, Object.keys(fields).length + groups.length, `${name}: field/group row count`);
    for (const [code, field] of Object.entries(fields)) {
        const row = rows.find(columns => columns[0] === code);
        assert.ok(row, `${name}: missing ${code}`);
        assert.equal(row[1], field.name, `${name}.${code}: name`);
        assert.equal(row[2].split(',')[0], field.format, `${name}.${code}: format`);
    }
    totals.fields += Object.keys(fields).length;
    totals.groups += groups.length;
    totals.derived += derived.length;
}

function validateLinks(name, document, totals) {
    for (const match of document.matchAll(/\]\(([^)]+)\)/g)) {
        const [target, fragment] = match[1].split('#');
        if (!target || /^[a-z]+:/i.test(target)) continue;
        const file = path.resolve(archaeology, decodeURIComponent(target));
        assert.ok(existsSync(file), `${name}: missing link ${target}`);
        if (/^L\d+$/.test(fragment ?? '')) {
            assert.ok(Number(fragment.slice(1)) <= readFileSync(file, 'utf8').split(/\r?\n/).length, `${name}: out-of-range ${match[1]}`);
        }
        totals.links += 1;
    }
}

export function validateEvidence(documentOverrides = {}) {
    const documents = {
        ...Object.fromEntries(artifacts.map(name => [name, readFileSync(path.join(archaeology, name), 'utf8')])),
        ...documentOverrides,
    };
    const members = readdirSync(library).filter(name => /\.(NSP|NSN|NSC|NSA|NSL|jcl)$/.test(name)).sort();
    const definitions = readdirSync(adabas).filter(name => /\.(ddm|txt)$/.test(name)).sort();
    assert.equal(members.length, 24, 'Library coverage changed');
    assert.equal(definitions.length, 5, 'Adabas coverage changed');
    const totals = { IF: 0, DECIDE: 0, REPORT: 0, ERROR: 0, CALLNAT: 0, INCLUDE: 0, USING: 0, fields: 0, groups: 0, derived: 0, variables: 0, links: 0 };
    Object.assign(totals, validateDispositions(documents['mysteries-found.md']));
    const sources = {};
    for (const name of members) {
        validateMember(name, documents, totals);
        const file = path.join(library, name);
        sources[path.relative(repository, file)] = checksum(file);
    }
    for (const name of definitions) {
        if (name.endsWith('.ddm')) validateDataFields(name, documents['data-map.md'], totals);
        const file = path.join(adabas, name);
        sources[path.relative(repository, file)] = checksum(file);
    }
    for (const [name, document] of Object.entries(documents)) validateLinks(name, document, totals);
    for (const [kind, expected] of Object.entries({ IF: 219, DECIDE: 15, REPORT: 8, ERROR: 17, CALLNAT: 9, INCLUDE: 9, USING: 23, fields: 199, groups: 7, derived: 14 })) {
        assert.equal(totals[kind], expected, `${kind}: baseline total`);
    }
    return {
        schema_version: 1,
        validation: 'static-documentary-evidence',
        generated_at: new Date().toISOString(),
        source_commit: execFileSync('/usr/bin/git', ['rev-parse', 'HEAD'], { cwd: repository, encoding: 'utf8' }).trim(),
        totals,
        source_sha256: sources,
        artifact_sha256: Object.fromEntries(artifacts.map(name => [name, checksum(path.join(archaeology, name))])),
        validator_sha256: checksum(fileURLToPath(import.meta.url)),
        validator_tests_sha256: checksum(path.join(archaeology, 'scripts/validate-evidence.test.mjs')),
        limitations: ['Not a Natural compiler or runtime test', 'No business-rule or human H1 approval', 'Historical document formats are not asserted equivalent'],
    };
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
    try {
        const report = validateEvidence();
        if (process.argv.includes('--write-report')) {
            const directory = path.join(archaeology, 'validation');
            mkdirSync(directory, { recursive: true });
            writeFileSync(path.join(directory, 'evidence.json'), `${JSON.stringify(report, null, 2)}\n`);
        }
        console.log(`PASS: ${JSON.stringify(report.totals)}`);
    } catch (error) {
        console.error(error.message);
        process.exitCode = 1;
    }
}