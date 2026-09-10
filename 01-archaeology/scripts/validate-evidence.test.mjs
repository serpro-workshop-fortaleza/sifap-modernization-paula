import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { controlBlocks, declaredVariables, validateEvidence } from './validate-evidence.mjs';

test('should_pair_nested_guards_and_ignore_commented_code', () => {
    const source = '* IF DISABLED\nIF READY\n  IF NO RECORDS FOUND\n  END-NOREC\nELSE\n  IGNORE\nEND-IF\n* END-IF';
    const result = controlBlocks(source);
    assert.deepEqual(result.IF, ['2-7', '3-4']);
});

test('should_record_decisions_report_hooks_and_error_handlers', () => {
    const source = 'DECIDE ON FIRST VALUE OF #TYPE\nNONE\nIGNORE\nEND-DECIDE\nAT END OF DATA\nIGNORE\nEND-ENDDATA\nON ERROR\nIGNORE\nEND-ERROR';
    const result = controlBlocks(source);
    assert.deepEqual(result, { IF: [], DECIDE: ['1-4'], REPORT: ['5-7'], ERROR: ['8-10'] });
});

test('should_reject_an_unpaired_end_marker', () => {
    assert.throws(() => controlBlocks('END-IF'), /Unpaired/);
});

test('should_reject_an_unclosed_guard', () => {
    assert.throws(() => controlBlocks('IF #COUNT = 0\nIGNORE'), /Unclosed IF/);
});

test('should_preserve_declaration_formats_and_exclude_comments_and_body', () => {
    const source = 'DEFINE DATA\n* 1 #EXAMPLE (N2)\n1 #ITEMS (P9.2/1:10)\n1 #VALID (L)\nEND-DEFINE\n1 #BODY (N4)';
    const result = declaredVariables(source);
    assert.deepEqual(result, { '#ITEMS': 'P9.2/1:10', '#VALID': 'L' });
});

test('should_validate_the_documented_corpus_without_treating_headers_as_fields', () => {
    const report = validateEvidence();
    assert.equal(report.totals.fields, 199);
    assert.equal(report.totals.variables, 537);
    assert.equal(Object.keys(report.source_sha256).length, 29);
});

test('should_reject_a_changed_control_interval', () => {
    const original = readFileSync(new URL('../reading-coverage.md', import.meta.url), 'utf8');
    const changed = original.replace('171-173; 256-259', '170-173; 256-259');
    assert.notEqual(changed, original);
    assert.throws(() => validateEvidence({ 'reading-coverage.md': changed }), /BATCHPGT.NSP: IF intervals/);
});

test('should_reject_a_changed_parameter_format', () => {
    const original = readFileSync(new URL('../program-data-dictionary.md', import.meta.url), 'utf8');
    const changed = original.replace('| #PV-MSG | A60 |', '| #PV-MSG | A61 |');
    assert.notEqual(changed, original);
    assert.throws(() => validateEvidence({ 'program-data-dictionary.md': changed }), /PDAVALID.NSA: declared variable/);
});

test('should_reject_a_changed_adabas_field_format', () => {
    const original = readFileSync(new URL('../data-map.md', import.meta.url), 'utf8');
    const changed = original.replace('| AB | NUM-CPF | A11 |', '| AB | NUM-CPF | A12 |');
    assert.notEqual(changed, original);
    assert.throws(() => validateEvidence({ 'data-map.md': changed }), /BENEFIC.ddm.AB: format/);
});

test('should_reject_a_missing_evidence_link', () => {
    assert.throws(() => validateEvidence({ 'inventory.md': '[Missing](legacy-sifap/absent.NSP)' }), /missing link/);
});

test('should_reject_an_out_of_range_source_line', () => {
    const changed = '[Invalid line](legacy-sifap/natural-programs/SUBVALNI.NSN#L99999)';
    assert.throws(() => validateEvidence({ 'inventory.md': changed }), /out-of-range/);
});