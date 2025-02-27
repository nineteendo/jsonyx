/* JSON speedups */
// TODO(Nice Zombies): speed up decoding
// https://github.com/benfred/py-spy#can-py-spy-profile-native-extensions
// https://github.com/P403n1x87/echion

#include <Python.h>
#include <stdbool.h> // bool

#define _Py_EnterRecursiveCall Py_EnterRecursiveCall
#define _Py_LeaveRecursiveCall Py_LeaveRecursiveCall

#if PY_VERSION_HEX < 0x03090000
#if !defined(PyObject_CallOneArg)
#define PyObject_CallOneArg(callable, arg) PyObject_CallFunctionObjArgs(callable, arg, NULL)
#endif
#endif /* PY_VERSION_HEX < 0x03090000 */

#if PY_VERSION_HEX < 0x03120000
#if !defined(Py_INFINITY)
#define Py_INFINITY Py_HUGE_VAL
#endif
#endif /* PY_VERSION_HEX < 0x03120000 */

typedef struct _PyScannerObject {
    PyObject_HEAD
    PyObject *Decimal;
    PyObject *bool_hook;
    PyObject *float_hook;
    PyObject *int_hook;
    PyObject *mapping_hook;
    PyObject *sequence_hook;
    PyObject *str_hook;
    int allow_comments;
    int allow_missing_commas;
    int allow_nan_and_infinity;
    int allow_surrogates;
    int allow_trailing_comma;
    int allow_unquoted_keys;
    int use_decimal;
} PyScannerObject;

#define PyScannerObject_CAST(op)    ((PyScannerObject *)(op))

typedef struct _PyEncoderObject {
    PyObject_HEAD
    PyObject *Decimal;
    PyObject *bool_types;
    PyObject *float_types;
    PyObject *indent;
    PyObject *int_types;
    PyObject *mapping_types;
    PyObject *sequence_types;
    PyObject *str_types;
    PyObject *end;
    PyObject *item_separator;
    PyObject *long_item_separator;
    PyObject *key_separator;
    Py_ssize_t max_indent_level;
    int allow_nan_and_infinity;
    int allow_surrogates;
    int ensure_ascii;
    int indent_leaves;
    int quoted_keys;
    int sort_keys;
    int trailing_comma;
} PyEncoderObject;

#define PyEncoderObject_CAST(op)    ((PyEncoderObject *)(op))

/* Forward decls */

static PyObject *
ascii_escape_unicode(PyObject *pystr, int allow_surrogates);
static PyObject *
scan_once_unicode(PyScannerObject *s, PyObject *memo, PyObject *pyfilename, PyObject *pystr, Py_ssize_t idx, Py_ssize_t *next_idx_ptr);
static PyObject *
scanner_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static void
scanner_dealloc(PyObject *self);
static int
scanner_clear(PyObject *self);
static PyObject *
encoder_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static void
encoder_dealloc(PyObject *self);
static int
encoder_clear(PyObject *self);
static int
encoder_listencode_sequence(PyEncoderObject *s, PyObject *markers, _PyUnicodeWriter *writer, PyObject *seq, Py_ssize_t indent_level, PyObject *indent_cache);
static int
encoder_listencode_obj(PyEncoderObject *s, PyObject *markers, _PyUnicodeWriter *writer, PyObject *obj, Py_ssize_t indent_level, PyObject *indent_cache);
static int
encoder_listencode_mapping(PyEncoderObject *s, PyObject *markers, _PyUnicodeWriter *writer, PyObject *mapping, Py_ssize_t indent_level, PyObject *indent_cache);
static void
raise_errmsg(const char *msg, PyObject *filename, PyObject *s, Py_ssize_t start, Py_ssize_t end);
static PyObject *
encoder_encode_string(PyEncoderObject *s, PyObject *obj);
static PyObject *
encoder_encode_float(PyEncoderObject *s, PyObject *obj);

#define S_CHAR(c) (c >= ' ' && c <= '~' && c != '\\' && c != '"')
#define IS_WHITESPACE(c) (((c) == ' ') || ((c) == '\t') || ((c) == '\n') || ((c) == '\r'))

static int
_skip_comments(PyScannerObject *s, PyObject *pyfilename, PyObject *pystr, Py_ssize_t *idx_ptr)
{
    const void *str;
    int kind;
    Py_ssize_t len;
    Py_ssize_t idx;
    Py_ssize_t comment_idx;

    str = PyUnicode_DATA(pystr);
    kind = PyUnicode_KIND(pystr);
    len = PyUnicode_GET_LENGTH(pystr);
    idx = *idx_ptr;
    while (1) {
        while (idx < len && IS_WHITESPACE(PyUnicode_READ(kind,str, idx))) {
            idx++;
        }
        comment_idx = idx;
        if (idx + 1 < len && PyUnicode_READ(kind, str, idx) == '/' &&
            PyUnicode_READ(kind, str, idx + 1) == '/')
        {
            idx += 2;
            while (idx < len && PyUnicode_READ(kind,str, idx) != '\n' && PyUnicode_READ(kind,str, idx) != '\r') {
                idx++;
            }
        }
        else if (idx + 1 < len && PyUnicode_READ(kind, str, idx) == '/' &&
                 PyUnicode_READ(kind, str, idx + 1) == '*')
        {
            idx += 2;
            while (1) {
                if (idx + 1 >= len) {
                    if (s->allow_comments) {
                        raise_errmsg("Unterminated comment", pyfilename, pystr, comment_idx, len);
                    }
                    else {
                        raise_errmsg("Comments are not allowed", pyfilename, pystr, comment_idx, len);
                    }
                    return -1;
                }
                if (PyUnicode_READ(kind,str, idx) == '*' &&
                    PyUnicode_READ(kind,str, idx + 1) == '/')
                {
                    break;
                }
                idx++;
            }
            idx += 2;
        }
        else {
            break;
        }
        if (!s->allow_comments) {
            raise_errmsg("Comments are not allowed", pyfilename, pystr, comment_idx, idx);
            return -1;
        }
    }
    *idx_ptr = idx;
    return 0;
}

static Py_ssize_t
ascii_escape_unichar(Py_UCS4 c, unsigned char *output, Py_ssize_t chars, int allow_surrogates)
{
    /* Escape unicode code point c to ASCII escape sequences
    in char *output. output must have at least 12 bytes unused to
    accommodate an escaped surrogate pair "\uXXXX\uXXXX" */
    output[chars++] = '\\';
    switch (c) {
        case '\\': output[chars++] = c; break;
        case '"': output[chars++] = c; break;
        case '\b': output[chars++] = 'b'; break;
        case '\f': output[chars++] = 'f'; break;
        case '\n': output[chars++] = 'n'; break;
        case '\r': output[chars++] = 'r'; break;
        case '\t': output[chars++] = 't'; break;
        default:
            if (c >= 0x10000) {
                /* UTF-16 surrogate pair */
                Py_UCS4 v = Py_UNICODE_HIGH_SURROGATE(c);
                output[chars++] = 'u';
                output[chars++] = Py_hexdigits[(v >> 12) & 0xf];
                output[chars++] = Py_hexdigits[(v >>  8) & 0xf];
                output[chars++] = Py_hexdigits[(v >>  4) & 0xf];
                output[chars++] = Py_hexdigits[(v      ) & 0xf];
                c = Py_UNICODE_LOW_SURROGATE(c);
                output[chars++] = '\\';
            }
            else if (0xd800 <= c && c <= 0xdfff && !allow_surrogates) {
                PyErr_SetString(PyExc_ValueError, "Surrogates are not allowed");
                return -1;
            }
            output[chars++] = 'u';
            output[chars++] = Py_hexdigits[(c >> 12) & 0xf];
            output[chars++] = Py_hexdigits[(c >>  8) & 0xf];
            output[chars++] = Py_hexdigits[(c >>  4) & 0xf];
            output[chars++] = Py_hexdigits[(c      ) & 0xf];
    }
    return chars;
}

static PyObject *
ascii_escape_unicode(PyObject *pystr, int allow_surrogates)
{
    /* Take a PyUnicode pystr and return a new ASCII-only escaped PyUnicode */
    Py_ssize_t i;
    Py_ssize_t input_chars;
    Py_ssize_t output_size;
    Py_ssize_t chars;
    PyObject *rval;
    const void *input;
    Py_UCS1 *output;
    int kind;

    input_chars = PyUnicode_GET_LENGTH(pystr);
    input = PyUnicode_DATA(pystr);
    kind = PyUnicode_KIND(pystr);

    /* Compute the output size */
    for (i = 0, output_size = 2; i < input_chars; i++) {
        Py_UCS4 c = PyUnicode_READ(kind, input, i);
        Py_ssize_t d;
        if (S_CHAR(c)) {
            d = 1;
        }
        else {
            switch(c) {
            case '\\': case '"': case '\b': case '\f':
            case '\n': case '\r': case '\t':
                d = 2; break;
            default:
                d = c >= 0x10000 ? 12 : 6;
            }
        }
        if (output_size > PY_SSIZE_T_MAX - d) {
            PyErr_SetString(PyExc_OverflowError, "string is too long to escape");
            return NULL;
        }
        output_size += d;
    }

    rval = PyUnicode_New(output_size, 127);
    if (rval == NULL) {
        return NULL;
    }
    output = PyUnicode_1BYTE_DATA(rval);
    chars = 0;
    output[chars++] = '"';
    for (i = 0; i < input_chars; i++) {
        Py_UCS4 c = PyUnicode_READ(kind, input, i);
        if (S_CHAR(c)) {
            output[chars++] = c;
        }
        else {
            chars = ascii_escape_unichar(c, output, chars, allow_surrogates);
            if (chars < 0) {
                return NULL;
            }
        }
    }
    output[chars++] = '"';
#ifdef Py_DEBUG
    assert(_PyUnicode_CheckConsistency(rval, 1));
#endif
    return rval;
}

static PyObject *
escape_unicode(PyObject *pystr)
{
    /* Take a PyUnicode pystr and return a new escaped PyUnicode */
    Py_ssize_t i;
    Py_ssize_t input_chars;
    Py_ssize_t output_size;
    Py_ssize_t chars;
    PyObject *rval;
    const void *input;
    int kind;
    Py_UCS4 maxchar;

    maxchar = PyUnicode_MAX_CHAR_VALUE(pystr);
    input_chars = PyUnicode_GET_LENGTH(pystr);
    input = PyUnicode_DATA(pystr);
    kind = PyUnicode_KIND(pystr);

    /* Compute the output size */
    for (i = 0, output_size = 2; i < input_chars; i++) {
        Py_UCS4 c = PyUnicode_READ(kind, input, i);
        Py_ssize_t d;
        switch (c) {
        case '\\': case '"': case '\b': case '\f':
        case '\n': case '\r': case '\t':
            d = 2;
            break;
        default:
            if (c <= 0x1f)
                d = 6;
            else
                d = 1;
        }
        if (output_size > PY_SSIZE_T_MAX - d) {
            PyErr_SetString(PyExc_OverflowError, "string is too long to escape");
            return NULL;
        }
        output_size += d;
    }

    rval = PyUnicode_New(output_size, maxchar);
    if (rval == NULL)
        return NULL;

    kind = PyUnicode_KIND(rval);

#define ENCODE_OUTPUT do { \
        chars = 0; \
        output[chars++] = '"'; \
        for (i = 0; i < input_chars; i++) { \
            Py_UCS4 c = PyUnicode_READ(kind, input, i); \
            switch (c) { \
            case '\\': output[chars++] = '\\'; output[chars++] = c; break; \
            case '"':  output[chars++] = '\\'; output[chars++] = c; break; \
            case '\b': output[chars++] = '\\'; output[chars++] = 'b'; break; \
            case '\f': output[chars++] = '\\'; output[chars++] = 'f'; break; \
            case '\n': output[chars++] = '\\'; output[chars++] = 'n'; break; \
            case '\r': output[chars++] = '\\'; output[chars++] = 'r'; break; \
            case '\t': output[chars++] = '\\'; output[chars++] = 't'; break; \
            default: \
                if (c <= 0x1f) { \
                    output[chars++] = '\\'; \
                    output[chars++] = 'u'; \
                    output[chars++] = '0'; \
                    output[chars++] = '0'; \
                    output[chars++] = Py_hexdigits[(c >> 4) & 0xf]; \
                    output[chars++] = Py_hexdigits[(c     ) & 0xf]; \
                } else { \
                    output[chars++] = c; \
                } \
            } \
        } \
        output[chars++] = '"'; \
    } while (0)

    if (kind == PyUnicode_1BYTE_KIND) {
        Py_UCS1 *output = PyUnicode_1BYTE_DATA(rval);
        ENCODE_OUTPUT;
    } else if (kind == PyUnicode_2BYTE_KIND) {
        Py_UCS2 *output = PyUnicode_2BYTE_DATA(rval);
        ENCODE_OUTPUT;
    } else {
        Py_UCS4 *output = PyUnicode_4BYTE_DATA(rval);
#ifdef Py_DEBUG
        assert(kind == PyUnicode_4BYTE_KIND);
#endif
        ENCODE_OUTPUT;
    }
#undef ENCODE_OUTPUT

#ifdef Py_DEBUG
    assert(_PyUnicode_CheckConsistency(rval, 1));
#endif
    return rval;
}

static void
raise_errmsg(const char *msg, PyObject *filename, PyObject *s, Py_ssize_t start, Py_ssize_t end)
{
    /* Use JSONSyntaxError exception to raise a nice looking SyntaxError subclass */
    PyObject *json = PyImport_ImportModule("jsonyx");
    if (json == NULL) {
        return;
    }
    PyObject *JSONSyntaxError = PyObject_GetAttrString(json, "JSONSyntaxError");
    Py_DECREF(json);
    if (JSONSyntaxError == NULL) {
        return;
    }

    PyObject *exc;
    exc = PyObject_CallFunction(JSONSyntaxError, "zOOnn", msg, filename, s, start, end);
    Py_DECREF(JSONSyntaxError);
    if (exc) {
        PyErr_SetObject(JSONSyntaxError, exc);
        Py_DECREF(exc);
    }
}

static PyObject *
scanstring_unicode(PyScannerObject *s, PyObject *pyfilename, PyObject *pystr, Py_ssize_t end, Py_ssize_t *next_end_ptr)
{
    /* Read the JSON string from PyUnicode pystr.
    end is the index of the first character after the quote.
    *next_end_ptr is a return-by-reference index of the character
        after the end quote

    Return value is a new PyUnicode
    */
    PyObject *old_rval = NULL;
    PyObject *rval = NULL;
    Py_ssize_t len;
    Py_ssize_t begin = end - 1;
    Py_ssize_t next /* = begin */;
    const void *buf;
    int kind;

    _PyUnicodeWriter writer;
    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;

    len = PyUnicode_GET_LENGTH(pystr);
    buf = PyUnicode_DATA(pystr);
    kind = PyUnicode_KIND(pystr);

    if (end < 0 || len < end) {
        PyErr_SetString(PyExc_ValueError, "end is out of bounds");
        goto bail;
    }
    while (1) {
        /* Find the end of the string or the next escape */
        Py_UCS4 c;
        {
            // Use tight scope variable to help register allocation.
            Py_UCS4 d = 0;
            for (next = end; next < len; next++) {
                d = PyUnicode_READ(kind, buf, next);
                if (d == '"' || d == '\\') {
                    break;
                }
                if (d <= 0x1f) {
                    if (d == '\n' || d == '\r') {
                        raise_errmsg("Unterminated string", pyfilename, pystr, begin, next);
                    }
                    else {
                        raise_errmsg("Unescaped control character", pyfilename, pystr, next, next + 1);
                    }
                    goto bail;
                }
            }
            c = d;
        }

        if (c != '"' && c != '\\') {
            raise_errmsg("Unterminated string", pyfilename, pystr, begin, next);
            goto bail;
        }

        /* Pick up this chunk if it's not zero length */
        if (next != end) {
            if (_PyUnicodeWriter_WriteSubstring(&writer, pystr, end, next) < 0) {
                goto bail;
            }
        }
        if (c == '"') {
            end = next;
            break;
        }
        next++;
        if (next == len) {
            raise_errmsg("Expecting escaped character", pyfilename, pystr, next, 0);
            goto bail;
        }
        c = PyUnicode_READ(kind, buf, next);
        if (c != 'u') {
            /* Non-unicode backslash escapes */
            end = next + 1;
            switch (c) {
                case '"': break;
                case '\\': break;
                case '/': break;
                case 'b': c = '\b'; break;
                case 'f': c = '\f'; break;
                case 'n': c = '\n'; break;
                case 'r': c = '\r'; break;
                case 't': c = '\t'; break;
                default:
                    if (c == '\n' || c == '\r') {
                        raise_errmsg("Expecting escaped character", pyfilename, pystr, end - 1, 0);
                    }
                    else {
                        raise_errmsg("Invalid backslash escape", pyfilename, pystr, end - 2, end);
                    }
                    goto bail;
            }
        }
        else {
            c = 0;
            next++;
            end = next + 4;
            if (end > len) {
                raise_errmsg("Expecting 4 hex digits", pyfilename, pystr, next, -4);
                goto bail;
            }
            /* Decode 4 hex digits */
            for (; next < end; next++) {
                Py_UCS4 digit = PyUnicode_READ(kind, buf, next);
                c <<= 4;
                switch (digit) {
                    case '0': case '1': case '2': case '3': case '4':
                    case '5': case '6': case '7': case '8': case '9':
                        c |= (digit - '0'); break;
                    case 'a': case 'b': case 'c': case 'd': case 'e':
                    case 'f':
                        c |= (digit - 'a' + 10); break;
                    case 'A': case 'B': case 'C': case 'D': case 'E':
                    case 'F':
                        c |= (digit - 'A' + 10); break;
                    default:
                        raise_errmsg("Expecting 4 hex digits", pyfilename, pystr, end - 4, -4);
                        goto bail;
                }
            }
            /* Surrogate pair */
            if (Py_UNICODE_IS_HIGH_SURROGATE(c)) {
                if (end + 2 < len &&
                    PyUnicode_READ(kind, buf, next++) == '\\' &&
                    PyUnicode_READ(kind, buf, next++) == 'u') {
                    if (end + 6 > len) {
                        raise_errmsg("Expecting 4 hex digits", pyfilename, pystr, end + 2, -4);
                        goto bail;
                    }
                    Py_UCS4 c2 = 0;
                    /* Decode 4 hex digits */
                    for (; next < end + 6; next++) {
                        Py_UCS4 digit = PyUnicode_READ(kind, buf, next);
                        c2 <<= 4;
                        switch (digit) {
                            case '0': case '1': case '2': case '3': case '4':
                            case '5': case '6': case '7': case '8': case '9':
                                c2 |= (digit - '0'); break;
                            case 'a': case 'b': case 'c': case 'd': case 'e':
                            case 'f':
                                c2 |= (digit - 'a' + 10); break;
                            case 'A': case 'B': case 'C': case 'D': case 'E':
                            case 'F':
                                c2 |= (digit - 'A' + 10); break;
                            default:
                                raise_errmsg("Expecting 4 hex digits", pyfilename, pystr, end + 2, -4);
                                goto bail;
                        }
                    }
                    if (Py_UNICODE_IS_LOW_SURROGATE(c2)) {
                        end += 6;
                        c = Py_UNICODE_JOIN_SURROGATES(c, c2);
                    }
                    else if (!s->allow_surrogates) {
                        raise_errmsg("Surrogates are not allowed", pyfilename, pystr, end - 6, end);
                        goto bail;
                    }
                }
                else if (!s->allow_surrogates) {
                    raise_errmsg("Surrogates are not allowed", pyfilename, pystr, end - 6, end);
                    goto bail;
                }
            }
            else if (Py_UNICODE_IS_LOW_SURROGATE(c) && !s->allow_surrogates) {
                raise_errmsg("Surrogates are not allowed", pyfilename, pystr, end - 6, end);
                goto bail;
            }
        }
        if (_PyUnicodeWriter_WriteChar(&writer, c) < 0) {
            goto bail;
        }
    }

#ifdef Py_DEBUG
    assert(end < len && PyUnicode_READ(kind, str, end) == '"');
#endif
    old_rval = _PyUnicodeWriter_Finish(&writer);
    if (s->str_hook != (PyObject *)&PyUnicode_Type) {
        rval = PyObject_CallOneArg(s->str_hook, old_rval);
        Py_DECREF(old_rval);
    }
    else {
        rval = old_rval;
    }
    *next_end_ptr = end + 1;
    return rval;

bail:
    *next_end_ptr = -1;
    _PyUnicodeWriter_Dealloc(&writer);
    return NULL;
}

static void
scanner_dealloc(PyObject *self)
{
    PyTypeObject *tp = Py_TYPE(self);
    /* bpo-31095: UnTrack is needed before calling any callbacks */
    PyObject_GC_UnTrack(self);
    (void)scanner_clear(self);
    tp->tp_free(self);
    Py_DECREF(tp);
}

static int
scanner_traverse(PyObject *op, visitproc visit, void *arg)
{
    PyScannerObject *self = PyScannerObject_CAST(op);
    Py_VISIT(Py_TYPE(self));
    Py_VISIT(self->bool_hook);
    Py_VISIT(self->float_hook);
    Py_VISIT(self->int_hook);
    Py_VISIT(self->mapping_hook);
    Py_VISIT(self->sequence_hook);
    Py_VISIT(self->str_hook);
    return 0;
}

static int
scanner_clear(PyObject *op)
{
    PyScannerObject *self = PyScannerObject_CAST(op);
    Py_CLEAR(self->bool_hook);
    Py_CLEAR(self->float_hook);
    Py_CLEAR(self->int_hook);
    Py_CLEAR(self->mapping_hook);
    Py_CLEAR(self->sequence_hook);
    Py_CLEAR(self->str_hook);
    return 0;
}

static PyObject *
_parse_object_unicode(PyScannerObject *s, PyObject *memo, PyObject *pyfilename, PyObject *pystr, Py_ssize_t idx, Py_ssize_t *next_idx_ptr)
{
    /* Read a JSON object from PyUnicode pystr.
    idx is the index of the first character after the opening curly brace.
    *next_idx_ptr is a return-by-reference index to the first character after
        the closing curly brace.

    Returns a new dict
    */
    const void *str;
    int kind;
    Py_ssize_t end_idx;
    PyObject *val = NULL;
    PyObject *rval = NULL;
    PyObject *key = NULL;
    int use_pairs = s->mapping_hook != (PyObject *)&PyDict_Type;
    Py_ssize_t next_idx;
    Py_ssize_t obj_idx = idx - 1;
    Py_ssize_t colon_idx;
    Py_ssize_t comma_idx;

    str = PyUnicode_DATA(pystr);
    kind = PyUnicode_KIND(pystr);
    end_idx = PyUnicode_GET_LENGTH(pystr) - 1;
    if (use_pairs)
        rval = PyList_New(0);
    else
        rval = PyDict_New();
    if (rval == NULL)
        return NULL;

    /* skip comments after { */
    if (_skip_comments(s, pyfilename, pystr, &idx) < 0) {
        goto bail;
    }

    /* only loop if the object is non-empty */
    if (idx > end_idx || PyUnicode_READ(kind, str, idx) != '}') {
        while (1) {
            PyObject *new_key;
            if (idx > end_idx) {
                raise_errmsg("Unterminated object", pyfilename, pystr, obj_idx, idx);
                goto bail;
            }

            /* read key */
            if (PyUnicode_READ(kind, str, idx) == '"') {
                key = scanstring_unicode(s, pyfilename, pystr, idx + 1, &next_idx);
            }
            else if (!Py_UNICODE_ISALPHA(PyUnicode_READ(kind, str, idx)) &&
                     PyUnicode_READ(kind, str, idx) != '_' &&
                     PyUnicode_READ(kind, str, idx) <= '\x7f')
            {
                raise_errmsg("Expecting key", pyfilename, pystr, idx, 0);
                goto bail;
            }
            else {
                next_idx = idx;
                next_idx++;
                while (next_idx <= end_idx && (Py_UNICODE_ISALNUM(PyUnicode_READ(kind, str, next_idx)) ||
                                               PyUnicode_READ(kind, str, next_idx) == '_' ||
                                               PyUnicode_READ(kind, str, next_idx) > '\x7f'))
                {
                    next_idx++;
                }
                key = PyUnicode_Substring(pystr, idx, next_idx);
                if (!PyUnicode_IsIdentifier(key)) {
                    raise_errmsg("Expecting key", pyfilename, pystr, idx, 0);
                    goto bail;
                }
                if (!s->allow_unquoted_keys) {
                    raise_errmsg("Unquoted keys are not allowed", pyfilename, pystr, idx, next_idx);
                    goto bail;
                }
            }
            if (key == NULL)
                goto bail;
            new_key = PyDict_SetDefault(memo, key, key);
            // This returns a borrowed reference, while new_key
            // is a strong reference in the case of PyObject_CallOneArg
            Py_INCREF(new_key);
            if (new_key == NULL)
                goto bail;

            Py_SETREF(key, new_key);
            colon_idx = idx = next_idx;

            /* skip comments between key and : delimiter, read :, skip comments */
            if (_skip_comments(s, pyfilename, pystr, &idx) < 0) {
                goto bail;
            }
            if (idx > end_idx || PyUnicode_READ(kind, str, idx) != ':') {
                raise_errmsg("Expecting colon", pyfilename, pystr, colon_idx, 0);
                goto bail;
            }
            idx++;
            if (_skip_comments(s, pyfilename, pystr, &idx) < 0) {
                goto bail;
            }

            /* read any JSON term */
            val = scan_once_unicode(s, memo, pyfilename, pystr, idx, &next_idx);
            if (val == NULL)
                goto bail;

            if (use_pairs) {
                PyObject *item = PyTuple_Pack(2, key, val);
                if (item == NULL)
                    goto bail;
                Py_CLEAR(key);
                Py_CLEAR(val);
                if (PyList_Append(rval, item) == -1) {
                    Py_DECREF(item);
                    goto bail;
                }
                Py_DECREF(item);
            }
            else {
                if (PyDict_SetItem(rval, key, val) < 0)
                    goto bail;
                Py_CLEAR(key);
                Py_CLEAR(val);
            }
            comma_idx = idx = next_idx;

            /* skip comments before } or , */
            if (_skip_comments(s, pyfilename, pystr, &idx) < 0) {
                goto bail;
            }

            /* bail if the object is closed or we didn't get the , delimiter */
            if (idx > end_idx) {
                raise_errmsg("Unterminated object", pyfilename, pystr, obj_idx, idx);
                goto bail;
            }
            if (PyUnicode_READ(kind, str, idx) == ',') {
                comma_idx = idx;
                idx++;

                /* skip comments after , delimiter */
                if (_skip_comments(s, pyfilename, pystr, &idx) < 0) {
                    goto bail;
                }
            }
            else if (PyUnicode_READ(kind, str, idx) == '}') {
                break;
            }
            else if (idx == comma_idx) {
                raise_errmsg("Expecting comma", pyfilename, pystr, comma_idx, 0);
                goto bail;
            }
            else if (!s->allow_missing_commas) {
                raise_errmsg("Missing commas are not allowed", pyfilename, pystr, comma_idx, 0);
                goto bail;
            }

            if (idx <= end_idx && PyUnicode_READ(kind, str, idx) == '}') {
                if (!s->allow_trailing_comma) {
                    raise_errmsg("Trailing comma is not allowed", pyfilename, pystr, comma_idx, comma_idx + 1);
                    goto bail;
                }
                break;
            }
        }
    }

#ifdef Py_DEBUG
    assert(idx <= end_idx && PyUnicode_READ(kind, str, idx) == '}');
#endif
    *next_idx_ptr = idx + 1;

    if (use_pairs) {
        val = PyObject_CallOneArg(s->mapping_hook, rval);
        Py_DECREF(rval);
        return val;
    }

    return rval;
bail:
    Py_XDECREF(key);
    Py_XDECREF(val);
    Py_XDECREF(rval);
    return NULL;
}

static PyObject *
_parse_array_unicode(PyScannerObject *s, PyObject *memo, PyObject *pyfilename, PyObject *pystr, Py_ssize_t idx, Py_ssize_t *next_idx_ptr) {
    /* Read a JSON array from PyUnicode pystr.
    idx is the index of the first character after the opening brace.
    *next_idx_ptr is a return-by-reference index to the first character after
        the closing brace.

    Returns a new PyList
    */
    const void *str;
    int kind;
    Py_ssize_t end_idx;
    PyObject *val = NULL;
    PyObject *rval;
    Py_ssize_t next_idx;
    Py_ssize_t arr_idx = idx - 1;
    Py_ssize_t comma_idx;

    rval = PyList_New(0);
    if (rval == NULL)
        return NULL;

    str = PyUnicode_DATA(pystr);
    kind = PyUnicode_KIND(pystr);
    end_idx = PyUnicode_GET_LENGTH(pystr) - 1;

    /* skip comments after [ */
    if (_skip_comments(s, pyfilename, pystr, &idx) < 0) {
        goto bail;
    }

    /* only loop if the array is non-empty */
    if (idx > end_idx || PyUnicode_READ(kind, str, idx) != ']') {
        while (1) {
            if (idx > end_idx) {
                raise_errmsg("Unterminated array", pyfilename, pystr, arr_idx, idx);
                goto bail;
            }

            /* read any JSON term  */
            val = scan_once_unicode(s, memo, pyfilename, pystr, idx, &next_idx);
            if (val == NULL)
                goto bail;

            if (PyList_Append(rval, val) < 0)
                goto bail;

            Py_CLEAR(val);
            comma_idx = idx = next_idx;

            /* skip comments between term and , */
            if (_skip_comments(s, pyfilename, pystr, &idx) < 0) {
                goto bail;
            }

            /* bail if the array is closed or we didn't get the , delimiter */
            if (idx > end_idx) {
                raise_errmsg("Unterminated array", pyfilename, pystr, arr_idx, idx);
                goto bail;
            }
            if (PyUnicode_READ(kind, str, idx) == ',') {
                comma_idx = idx;
                idx++;

                /* skip comments after , */
                if (_skip_comments(s, pyfilename, pystr, &idx) < 0) {
                    goto bail;
                }
            }
            else if (PyUnicode_READ(kind, str, idx) == ']') {
                break;
            }
            else if (idx == comma_idx) {
                raise_errmsg("Expecting comma", pyfilename, pystr, comma_idx, 0);
                goto bail;
            }
            else if (!s->allow_missing_commas) {
                raise_errmsg("Missing commas are not allowed", pyfilename, pystr, comma_idx, 0);
                goto bail;
            }

            if (idx <= end_idx && PyUnicode_READ(kind, str, idx) == ']') {
                if (!s->allow_trailing_comma) {
                    raise_errmsg("Trailing comma is not allowed", pyfilename, pystr, comma_idx, comma_idx + 1);
                    goto bail;
                }
                break;
            }
        }
    }

#ifdef Py_DEBUG
    assert(idx <= end_idx && PyUnicode_READ(kind, str, idx) == ']');
#endif
    *next_idx_ptr = idx + 1;
    if (s->sequence_hook != (PyObject *)&PyList_Type) {
        val = PyObject_CallOneArg(s->sequence_hook, rval);
        Py_DECREF(rval);
        return val;
    }
    return rval;
bail:
    Py_XDECREF(val);
    Py_DECREF(rval);
    return NULL;
}

static PyObject *
_match_number_unicode(PyScannerObject *s, PyObject *pyfilename, PyObject *pystr, Py_ssize_t start, Py_ssize_t *next_idx_ptr) {
    /* Read a JSON number from PyUnicode pystr.
    idx is the index of the first character of the number
    *next_idx_ptr is a return-by-reference index to the first character after
        the number.

    Returns a new PyObject representation of that number: PyLong, or PyFloat.
    */
    const void *str;
    int kind;
    Py_ssize_t end_idx;
    Py_ssize_t idx = start;
    int is_float = 0;
    PyObject *old_rval;
    PyObject *rval;
    PyObject *numstr = NULL;

    str = PyUnicode_DATA(pystr);
    kind = PyUnicode_KIND(pystr);
    end_idx = PyUnicode_GET_LENGTH(pystr) - 1;

    /* read a sign if it's there, make sure it's not the end of the string */
    if (PyUnicode_READ(kind, str, idx) == '-') {
        idx++;
        if (idx > end_idx) {
            raise_errmsg("Expecting value", pyfilename, pystr, start, 0);
            return NULL;
        }
    }

    /* read as many integer digits as we find as long as it doesn't start with 0 */
    if (PyUnicode_READ(kind, str, idx) >= '1' && PyUnicode_READ(kind, str, idx) <= '9') {
        idx++;
        while (idx <= end_idx && PyUnicode_READ(kind, str, idx) >= '0' && PyUnicode_READ(kind, str, idx) <= '9') idx++;
    }
    /* if it starts with 0 we only expect one integer digit */
    else if (PyUnicode_READ(kind, str, idx) == '0') {
        idx++;
    }
    /* no integer digits, error */
    else {
        raise_errmsg("Expecting value", pyfilename, pystr, start, 0);
        return NULL;
    }

    /* if the next char is '.' followed by a digit then read all float digits */
    if (idx < end_idx && PyUnicode_READ(kind, str, idx) == '.' && PyUnicode_READ(kind, str, idx + 1) >= '0' && PyUnicode_READ(kind, str, idx + 1) <= '9') {
        is_float = 1;
        idx += 2;
        while (idx <= end_idx && PyUnicode_READ(kind, str, idx) >= '0' && PyUnicode_READ(kind, str, idx) <= '9') idx++;
    }

    /* if the next char is 'e' or 'E' then maybe read the exponent (or backtrack) */
    if (idx < end_idx && (PyUnicode_READ(kind, str, idx) == 'e' || PyUnicode_READ(kind, str, idx) == 'E')) {
        Py_ssize_t e_start = idx;
        idx++;

        /* read an exponent sign if present */
        if (idx < end_idx && (PyUnicode_READ(kind, str, idx) == '-' || PyUnicode_READ(kind, str, idx) == '+')) idx++;

        /* read all digits */
        while (idx <= end_idx && PyUnicode_READ(kind, str, idx) >= '0' && PyUnicode_READ(kind, str, idx) <= '9') idx++;

        /* if we got a digit, then parse as float. if not, backtrack */
        if (PyUnicode_READ(kind, str, idx - 1) >= '0' && PyUnicode_READ(kind, str, idx - 1) <= '9') {
            is_float = 1;
        }
        else {
            idx = e_start;
        }
    }

    if (is_float && s->use_decimal) {
        /* copy the section we determined to be a number */
        numstr = PyUnicode_FromKindAndData(kind,
                                           (char*)str + kind * start,
                                           idx - start);
        if (numstr == NULL)
            return NULL;
        rval = PyObject_CallOneArg(s->Decimal, numstr);
        if (PyErr_ExceptionMatches(PyExc_ArithmeticError)) {
            PyErr_Clear();
            raise_errmsg("Number is too big", pyfilename, pystr, start, idx);
            goto bail;
        }
    }
    else {
        Py_ssize_t i, n;
        char *buf;
        /* Straight conversion to ASCII, to avoid costly conversion of
            decimal unicode digits (which cannot appear here) */
        n = idx - start;
        numstr = PyBytes_FromStringAndSize(NULL, n);
        if (numstr == NULL)
            return NULL;
        buf = PyBytes_AS_STRING(numstr);
        for (i = 0; i < n; i++) {
            buf[i] = (char) PyUnicode_READ(kind, str, i + start);
        }
        if (is_float) {
            old_rval = PyFloat_FromString(numstr);
            if (!isfinite(PyFloat_AS_DOUBLE(old_rval))) {
                Py_DECREF(old_rval);
                raise_errmsg("Big numbers require decimal", pyfilename, pystr, start, idx);
                goto bail;
            }
            if (s->float_hook != (PyObject *)&PyFloat_Type) {
                rval = PyObject_CallOneArg(s->float_hook, old_rval);
                Py_DECREF(old_rval);
            }
            else {
                rval = old_rval;
            }
        }
        else {
            old_rval = PyLong_FromString(buf, NULL, 10);
            if (PyErr_ExceptionMatches(PyExc_ValueError)) {
                PyErr_Clear();
                raise_errmsg("Number is too big", pyfilename, pystr, start, idx);
                goto bail;
            }
            if (s->int_hook != (PyObject *)&PyLong_Type) {
                rval = PyObject_CallOneArg(s->int_hook, old_rval);
                Py_DECREF(old_rval);
            }
            else {
                rval = old_rval;
            }
        }
    }
    Py_DECREF(numstr);
    *next_idx_ptr = idx;
    return rval;
bail:
    Py_DECREF(numstr);
    return NULL;
}

static PyObject *
scan_once_unicode(PyScannerObject *s, PyObject *memo, PyObject *pyfilename, PyObject *pystr, Py_ssize_t idx, Py_ssize_t *next_idx_ptr)
{
    /* Read one JSON term (of any kind) from PyUnicode pystr.
    idx is the index of the first character of the term
    *next_idx_ptr is a return-by-reference index to the first character after
        the number.

    Returns a new PyObject representation of the term.
    */
    PyObject *old_res;
    PyObject *res;
    const void *str;
    int kind;
    Py_ssize_t length;

    str = PyUnicode_DATA(pystr);
    kind = PyUnicode_KIND(pystr);
    length = PyUnicode_GET_LENGTH(pystr);

    if (idx < 0) {
        PyErr_SetString(PyExc_ValueError, "idx cannot be negative");
        return NULL;
    }
    if (idx >= length) {
        raise_errmsg("Expecting value", pyfilename, pystr, idx, 0);
        return NULL;
    }

    switch (PyUnicode_READ(kind, str, idx)) {
        case '"':
            /* string */
            return scanstring_unicode(s, pyfilename, pystr, idx + 1, next_idx_ptr);
        case '{':
            /* object */
            if (_Py_EnterRecursiveCall(" while decoding a JSON object "
                                       "from a unicode string"))
                return NULL;
            res = _parse_object_unicode(s, memo, pyfilename, pystr, idx + 1, next_idx_ptr);
            _Py_LeaveRecursiveCall();
            return res;
        case '[':
            /* array */
            if (_Py_EnterRecursiveCall(" while decoding a JSON array "
                                       "from a unicode string"))
                return NULL;
            res = _parse_array_unicode(s, memo, pyfilename, pystr, idx + 1, next_idx_ptr);
            _Py_LeaveRecursiveCall();
            return res;
        case 'n':
            /* null */
            if ((idx + 3 < length) && PyUnicode_READ(kind, str, idx + 1) == 'u' && PyUnicode_READ(kind, str, idx + 2) == 'l' && PyUnicode_READ(kind, str, idx + 3) == 'l') {
                *next_idx_ptr = idx + 4;
                Py_RETURN_NONE;
            }
            break;
        case 't':
            /* true */
            if ((idx + 3 < length) && PyUnicode_READ(kind, str, idx + 1) == 'r' && PyUnicode_READ(kind, str, idx + 2) == 'u' && PyUnicode_READ(kind, str, idx + 3) == 'e') {
                *next_idx_ptr = idx + 4;
                if (s->bool_hook != (PyObject *)&PyBool_Type) {
                    return PyObject_CallOneArg(s->bool_hook, Py_True);
                }
                Py_RETURN_TRUE;
            }
            break;
        case 'f':
            /* false */
            if ((idx + 4 < length) && PyUnicode_READ(kind, str, idx + 1) == 'a' &&
                PyUnicode_READ(kind, str, idx + 2) == 'l' &&
                PyUnicode_READ(kind, str, idx + 3) == 's' &&
                PyUnicode_READ(kind, str, idx + 4) == 'e') {
                *next_idx_ptr = idx + 5;
                if (s->bool_hook != (PyObject *)&PyBool_Type) {
                    return PyObject_CallOneArg(s->bool_hook, Py_False);
                }
                Py_RETURN_FALSE;
            }
            break;
        case 'N':
            /* NaN */
            if ((idx + 2 < length) && PyUnicode_READ(kind, str, idx + 1) == 'a' &&
                PyUnicode_READ(kind, str, idx + 2) == 'N') {
                if (!s->allow_nan_and_infinity) {
                    raise_errmsg("NaN is not allowed", pyfilename, pystr, idx, idx + 3);
                    return NULL;
                }
                *next_idx_ptr = idx + 3;
                if (s->use_decimal) {
                    old_res = PyUnicode_FromString("NaN");
                    if (old_res == NULL) {
                        return NULL;
                    }
                    res = PyObject_CallOneArg(s->Decimal, old_res);
                    Py_DECREF(old_res);
                    return res;
                }
                if (s->float_hook != (PyObject *)&PyFloat_Type) {
                    old_res = PyFloat_FromDouble(Py_NAN);
                    if (old_res == NULL) {
                        return NULL;
                    }
                    res = PyObject_CallOneArg(s->float_hook, old_res);
                    Py_DECREF(old_res);
                    return res;
                }
                Py_RETURN_NAN;
            }
            break;
        case 'I':
            /* Infinity */
            if ((idx + 7 < length) && PyUnicode_READ(kind, str, idx + 1) == 'n' &&
                PyUnicode_READ(kind, str, idx + 2) == 'f' &&
                PyUnicode_READ(kind, str, idx + 3) == 'i' &&
                PyUnicode_READ(kind, str, idx + 4) == 'n' &&
                PyUnicode_READ(kind, str, idx + 5) == 'i' &&
                PyUnicode_READ(kind, str, idx + 6) == 't' &&
                PyUnicode_READ(kind, str, idx + 7) == 'y') {
                if (!s->allow_nan_and_infinity) {
                    raise_errmsg("Infinity is not allowed", pyfilename, pystr, idx, idx + 8);
                    return NULL;
                }
                *next_idx_ptr = idx + 8;
                if (s->use_decimal) {
                    old_res = PyUnicode_FromString("Infinity");
                    if (old_res == NULL) {
                        return NULL;
                    }
                    res = PyObject_CallOneArg(s->Decimal, old_res);
                    Py_DECREF(old_res);
                    return res;
                }
                if (s->float_hook != (PyObject *)&PyFloat_Type) {
                    old_res = PyFloat_FromDouble(+Py_INFINITY);
                    if (old_res == NULL) {
                        return NULL;
                    }
                    res = PyObject_CallOneArg(s->float_hook, old_res);
                    Py_DECREF(old_res);
                    return res;
                }
                Py_RETURN_INF(+1);
            }
            break;
        case '-':
            /* -Infinity */
            if ((idx + 8 < length) && PyUnicode_READ(kind, str, idx + 1) == 'I' &&
                PyUnicode_READ(kind, str, idx + 2) == 'n' &&
                PyUnicode_READ(kind, str, idx + 3) == 'f' &&
                PyUnicode_READ(kind, str, idx + 4) == 'i' &&
                PyUnicode_READ(kind, str, idx + 5) == 'n' &&
                PyUnicode_READ(kind, str, idx + 6) == 'i' &&
                PyUnicode_READ(kind, str, idx + 7) == 't' &&
                PyUnicode_READ(kind, str, idx + 8) == 'y') {
                *next_idx_ptr = idx + 9;
                if (!s->allow_nan_and_infinity) {
                    raise_errmsg("-Infinity is not allowed", pyfilename, pystr, idx, idx + 9);
                    return NULL;
                }
                if (s->use_decimal) {
                    old_res = PyUnicode_FromString("-Infinity");
                    if (old_res == NULL) {
                        return NULL;
                    }
                    res = PyObject_CallOneArg(s->Decimal, old_res);
                    Py_DECREF(old_res);
                    return res;
                }
                if (s->float_hook != (PyObject *)&PyFloat_Type) {
                    old_res = PyFloat_FromDouble(-Py_INFINITY);
                    if (old_res == NULL) {
                        return NULL;
                    }
                    res = PyObject_CallOneArg(s->float_hook, old_res);
                    Py_DECREF(old_res);
                    return res;
                }
                Py_RETURN_INF(-1);
            }
            break;
    }
    /* Didn't find a string, object, array, or named constant. Look for a number. */
    return _match_number_unicode(s, pyfilename, pystr, idx, next_idx_ptr);
}

static PyObject *
scanner_call(PyObject *op, PyObject *args, PyObject *kwds)
{
    PyScannerObject *self = PyScannerObject_CAST(op);
    /* Python callable interface to scan_once_{str,unicode} */
    PyObject *pyfilename;
    PyObject *pystr;
    PyObject *rval;
    Py_ssize_t len;
    Py_ssize_t idx = 0;
    Py_ssize_t next_idx = -1;
    static char *kwlist[] = {"filename", "string", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "UU:scanner", kwlist, &pyfilename, &pystr)) {
        return NULL;
    }
    len = PyUnicode_GET_LENGTH(pystr);
    if (len > 0 && PyUnicode_READ_CHAR(pystr, 0) == L'\ufeff') {
        raise_errmsg("Unexpected UTF-8 BOM", pyfilename, pystr, 0, 1);
        return NULL;
    }
    if (_skip_comments(self, pyfilename, pystr, &idx) < 0)
    {
        return NULL;
    }
    PyObject *memo = PyDict_New();
    if (memo == NULL) {
        return NULL;
    }
    rval = scan_once_unicode(self, memo, pyfilename, pystr, idx, &next_idx);
    Py_DECREF(memo);
    if (rval == NULL) {
        return NULL;
    }
    idx = next_idx;
    if (_skip_comments(self, pyfilename, pystr, &idx) < 0) {
        return NULL;
    }
    if (idx < len) {
        raise_errmsg("Expecting end of file", pyfilename, pystr, idx, 0);
        return NULL;
    }
    return rval;
}

static PyObject *
scanner_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"bool_hook", "float_hook", "int_hook",
                             "mapping_hook", "sequence_hook", "str_hook",
                             "allow_comments", "allow_missing_commas",
                             "allow_nan_and_infinity", "allow_surrogates",
                             "allow_trailing_comma", "allow_unquoted_keys",
                             "use_decimal", NULL};

    PyScannerObject *s;
    PyObject *bool_hook, *float_hook, *int_hook, *mapping_hook, *sequence_hook;
    PyObject *str_hook;
    int allow_comments, allow_missing_commas, allow_nan_and_infinity;
    int allow_surrogates, allow_trailing_comma, allow_unquoted_keys;
    int use_decimal;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOOOOOppppppp:make_scanner", kwlist,
        &bool_hook, &float_hook, &int_hook, &mapping_hook, &sequence_hook,
        &str_hook,
        &allow_comments, &allow_missing_commas, &allow_nan_and_infinity,
        &allow_surrogates, &allow_trailing_comma, &allow_unquoted_keys,
        &use_decimal))
        return NULL;

    s = (PyScannerObject *)type->tp_alloc(type, 0);
    if (s == NULL) {
        return NULL;
    }

    PyObject *decimal = PyImport_ImportModule((char *) "decimal");
    if (decimal == NULL) {
        goto bail;
    }
    s->Decimal = PyObject_GetAttrString(decimal, (char *) "Decimal");
    Py_DECREF(decimal);
    if (s->Decimal == NULL) {
        goto bail;
    }
    s->bool_hook = bool_hook;
    s->float_hook = float_hook;
    s->int_hook = int_hook;
    s->mapping_hook = mapping_hook;
    s->sequence_hook = sequence_hook;
    s->str_hook = str_hook;
    s->allow_comments = allow_comments;
    s->allow_missing_commas = allow_missing_commas;
    s->allow_nan_and_infinity = allow_nan_and_infinity;
    s->allow_surrogates = allow_surrogates;
    s->allow_trailing_comma = allow_trailing_comma;
    s->allow_unquoted_keys = allow_unquoted_keys;
    s->use_decimal = use_decimal;
    Py_INCREF(s->bool_hook);
    Py_INCREF(s->float_hook);
    Py_INCREF(s->int_hook);
    Py_INCREF(s->mapping_hook);
    Py_INCREF(s->sequence_hook);
    Py_INCREF(s->str_hook);
    return (PyObject *)s;

bail:
    Py_DECREF(s);
    return NULL;
}

PyDoc_STRVAR(scanner_doc, "Make JSON scanner");

static PyType_Slot PyScannerType_slots[] = {
    {Py_tp_doc, (void *)scanner_doc},
    {Py_tp_dealloc, scanner_dealloc},
    {Py_tp_call, scanner_call},
    {Py_tp_traverse, scanner_traverse},
    {Py_tp_clear, scanner_clear},
    {Py_tp_new, scanner_new},
    {0, 0}
};

static PyType_Spec PyScannerType_spec = {
    .name = "_jsonyx.Scanner",
    .basicsize = sizeof(PyScannerObject),
    .itemsize = 0,
    .flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
    .slots = PyScannerType_slots,
};

static PyObject *
encoder_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"bool_types", "float_types", "indent",
                             "int_types", "mapping_types", "sequence_types",
                             "str_types", "end", "item_separator",
                             "long_item_separator", "key_separator",
                             "max_indent_level", "allow_nan_and_infinity",
                             "allow_surrogates", "ensure_ascii",
                             "indent_leaves", "quoted_keys", "sort_keys",
                             "trailing_comma", NULL};

    PyEncoderObject *s;
    PyObject *bool_types, *float_types, *indent, *int_types, *mapping_types;
    PyObject *sequence_types, *str_types;
    PyObject *end, *item_separator, *long_item_separator, *key_separator;
    Py_ssize_t max_indent_level;
    int allow_nan_and_infinity, allow_surrogates, ensure_ascii, indent_leaves;
    int quoted_keys, sort_keys, trailing_comma;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOOOOOOUUUUnppppppp:make_encoder", kwlist,
        &bool_types, &float_types, &indent, &int_types, &mapping_types,
        &sequence_types, &str_types, &end, &item_separator,
        &long_item_separator, &key_separator,
        &max_indent_level,
        &allow_nan_and_infinity, &allow_surrogates, &ensure_ascii,
        &indent_leaves, &quoted_keys, &sort_keys, &trailing_comma))
        return NULL;

    s = (PyEncoderObject *)type->tp_alloc(type, 0);
    if (s == NULL)
        return NULL;

    PyObject *decimal = PyImport_ImportModule((char *) "decimal");
    if (decimal == NULL) {
        goto bail;
    }
    s->Decimal = PyObject_GetAttrString(decimal, (char *) "Decimal");
    Py_DECREF(decimal);
    if (s->Decimal == NULL) {
        goto bail;
    }
    s->bool_types = bool_types;
    s->float_types = float_types;
    s->indent = indent;
    s->int_types = int_types;
    s->mapping_types = mapping_types;
    s->sequence_types = sequence_types;
    s->str_types = str_types;
    s->end = end;
    s->item_separator = item_separator;
    s->long_item_separator = long_item_separator;
    s->key_separator = key_separator;
    s->max_indent_level = max_indent_level;
    s->allow_nan_and_infinity = allow_nan_and_infinity;
    s->allow_surrogates = allow_surrogates;
    s->ensure_ascii = ensure_ascii;
    s->indent_leaves = indent_leaves;
    s->quoted_keys = quoted_keys;
    s->sort_keys = sort_keys;
    s->trailing_comma = trailing_comma;
    Py_INCREF(s->bool_types);
    Py_INCREF(s->float_types);
    Py_INCREF(s->indent);
    Py_INCREF(s->int_types);
    Py_INCREF(s->mapping_types);
    Py_INCREF(s->sequence_types);
    Py_INCREF(s->str_types);
    Py_INCREF(s->end);
    Py_INCREF(s->item_separator);
    Py_INCREF(s->long_item_separator);
    Py_INCREF(s->key_separator);
    return (PyObject *)s;

bail:
    Py_DECREF(s);
    return NULL;
}


/* indent_cache is a list that contains intermixed values at even and odd
 * positions:
 *
 * 2*k   : '\n' + indent * k
 *         strings written after opening and before closing brackets
 * 2*k-1 : item_separator + '\n' + indent * k
 *         strings written between items
 *
 * Its size is always an odd number.
 */
static PyObject *
create_indent_cache(PyEncoderObject *s)
{
    PyObject *newline_indent = PyUnicode_FromOrdinal('\n');
    if (newline_indent == NULL) {
        return NULL;
    }
    PyObject *indent_cache = PyList_New(1);
    if (indent_cache == NULL) {
        Py_DECREF(newline_indent);
        return NULL;
    }
    PyList_SET_ITEM(indent_cache, 0, newline_indent);
    return indent_cache;
}

/* Extend indent_cache by adding values for the next level.
 * It should have values for the indent_level-1 level before the call.
 */
static int
update_indent_cache(PyEncoderObject *s,
                    Py_ssize_t indent_level, PyObject *indent_cache)
{
    assert(indent_level * 2 == PyList_GET_SIZE(indent_cache) + 1);
    assert(indent_level > 0);
    PyObject *newline_indent = PyList_GET_ITEM(indent_cache, (indent_level - 1)*2);
    newline_indent = PyUnicode_Concat(newline_indent, s->indent);
    if (newline_indent == NULL) {
        return -1;
    }
    PyObject *separator_indent = PyUnicode_Concat(s->item_separator, newline_indent);
    if (separator_indent == NULL) {
        Py_DECREF(newline_indent);
        return -1;
    }
    if (PyList_Append(indent_cache, separator_indent) < 0 ||
        PyList_Append(indent_cache, newline_indent) < 0)
    {
        Py_DECREF(separator_indent);
        Py_DECREF(newline_indent);
        return -1;
    }
    Py_DECREF(separator_indent);
    Py_DECREF(newline_indent);
    return 0;
}

static PyObject *
get_item_separator(PyEncoderObject *s,
                   Py_ssize_t indent_level, PyObject *indent_cache)
{
    assert(indent_level > 0);
    if (indent_level * 2 > PyList_GET_SIZE(indent_cache)) {
        if (update_indent_cache(s, indent_level, indent_cache) < 0) {
            return NULL;
        }
    }
    assert(indent_level * 2 < PyList_GET_SIZE(indent_cache));
    return PyList_GET_ITEM(indent_cache, indent_level * 2 - 1);
}

static int
write_newline_indent(_PyUnicodeWriter *writer,
                     Py_ssize_t indent_level, PyObject *indent_cache)
{
    PyObject *newline_indent = PyList_GET_ITEM(indent_cache, indent_level * 2);
    return _PyUnicodeWriter_WriteStr(writer, newline_indent);
}


static PyObject *
encoder_call(PyObject *op, PyObject *args, PyObject *kwds)
{
    /* Python callable interface to encode_listencode_obj */
    static char *kwlist[] = {"obj", NULL};
    PyObject *obj;
    _PyUnicodeWriter writer;
    PyEncoderObject *self = PyEncoderObject_CAST(op);

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O:encode", kwlist,
        &obj))
        return NULL;

    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;

    PyObject *indent_cache = NULL;
    PyObject *markers = NULL;
    if (self->indent != Py_None) {
        indent_cache = create_indent_cache(self);
        if (indent_cache == NULL) {
            goto bail;
        }
    }
    markers = PyDict_New();
    if (markers == NULL ||
        encoder_listencode_obj(self, markers, &writer, obj, 0, indent_cache))
    {
        goto bail;
    }

    Py_DECREF(markers);
    if (_PyUnicodeWriter_WriteStr(&writer, self->end) < 0) {
        goto bail;
    }
    return _PyUnicodeWriter_Finish(&writer);

bail:
    _PyUnicodeWriter_Dealloc(&writer);
    Py_XDECREF(indent_cache);
    Py_XDECREF(markers);
    return NULL;
}

static PyObject *
encoder_encode_float(PyEncoderObject *s, PyObject *obj)
{
    /* Return the JSON representation of a PyFloat. */
    double i = PyFloat_AS_DOUBLE(obj);
    if (isfinite(i)) {
        return PyFloat_Type.tp_repr(obj);
    }
    else if (!s->allow_nan_and_infinity) {
        PyErr_Format(
                PyExc_ValueError,
                "%R is not allowed",
                obj
                );
        return NULL;
    }
    if (i > 0) {
        return PyUnicode_FromString("Infinity");
    }
    else if (i < 0) {
        return PyUnicode_FromString("-Infinity");
    }
    else {
        return PyUnicode_FromString("NaN");
    }
}

static PyObject *
encoder_encode_decimal(PyEncoderObject *s, PyObject *obj)
{
    /* Return the JSON representation of a Decimal. */
    PyObject *is_finite = PyObject_CallMethod(obj, "is_finite", NULL);
    if (is_finite == NULL) {
        return NULL;
    }

    if (!PyObject_IsTrue(is_finite)) {
        Py_DECREF(is_finite);
        PyObject *is_snan = PyObject_CallMethod(obj, "is_snan", NULL);
        if (is_snan == NULL) {
            return NULL;
        }

        if (PyObject_IsTrue(is_snan)) {
            Py_DECREF(is_snan);
            PyErr_Format(PyExc_ValueError, "%R is not JSON serializable", obj);
            return NULL;
        }

        Py_DECREF(is_snan);
        if (!s->allow_nan_and_infinity) {
            PyErr_Format(PyExc_ValueError, "%R is not allowed", obj);
            return NULL;
        }

        PyObject *is_qnan = PyObject_CallMethod(obj, "is_qnan", NULL);
        if (is_qnan == NULL) {
            return NULL;
        }

        if (PyObject_IsTrue(is_qnan)) {
            Py_DECREF(is_qnan);
            return PyUnicode_FromString("NaN");
        }

        Py_DECREF(is_qnan);
    }

    Py_DECREF(is_finite);
    return PyObject_Str(obj);
}

static PyObject *
encoder_encode_string(PyEncoderObject *s, PyObject *obj)
{
    /* Return the JSON representation of a string */
    if (!s->ensure_ascii) {
        return escape_unicode(obj);
    }
    else {
        return ascii_escape_unicode(obj, s->allow_surrogates);
    }
}

static int
_steal_accumulate(_PyUnicodeWriter *writer, PyObject *stolen)
{
    /* Append stolen and then decrement its reference count */
    int rval = _PyUnicodeWriter_WriteStr(writer, stolen);
    Py_DECREF(stolen);
    return rval;
}

static int
encoder_listencode_obj(PyEncoderObject *s, PyObject *markers, _PyUnicodeWriter *writer,
                       PyObject *obj,
                       Py_ssize_t indent_level, PyObject *indent_cache)
{
    /* Encode Python object obj to a JSON term */
    PyObject *new_obj;
    int rv;

    if (obj == Py_None) {
      return _PyUnicodeWriter_WriteASCIIString(writer, "null", 4);
    }
    else if (obj == Py_True || obj == Py_False || PyObject_IsInstance(obj, s->bool_types)) {
        if (PyErr_Occurred())
            return -1;
        rv = PyObject_IsTrue(obj);
        if (rv == -1) {
            return -1;
        }
        else if (rv) {
            return _PyUnicodeWriter_WriteASCIIString(writer, "true", 4);
        }
        else {
            return _PyUnicodeWriter_WriteASCIIString(writer, "false", 5);
        }
    }
    else if (PyUnicode_Check(obj) || PyObject_IsInstance(obj, s->str_types)) {
        if (PyErr_Occurred())
            return -1;
        new_obj = PyObject_Str(obj);
        if (new_obj == NULL)
            return -1;
        PyObject *encoded = encoder_encode_string(s, new_obj);
        Py_DECREF(new_obj);
        if (encoded == NULL)
            return -1;
        return _steal_accumulate(writer, encoded);
    }
    else if (PyLong_Check(obj) || PyObject_IsInstance(obj, s->int_types)) {
        if (PyErr_Occurred())
            return -1;
        new_obj = PyNumber_Long(obj);
        if (new_obj == NULL)
            return -1;
        PyObject *encoded = PyLong_Type.tp_repr(new_obj);
        Py_DECREF(new_obj);
        if (encoded == NULL)
            return -1;
        return _steal_accumulate(writer, encoded);
    }
    else if (PyFloat_Check(obj) || PyObject_IsInstance(obj, s->float_types)) {
        if (PyErr_Occurred())
            return -1;
        new_obj = PyNumber_Float(obj);
        if (new_obj == NULL)
            return -1;
        PyObject *encoded = encoder_encode_float(s, new_obj);
        Py_DECREF(new_obj);
        if (encoded == NULL)
            return -1;
        return _steal_accumulate(writer, encoded);
    }
    else if (PyList_Check(obj) || PyTuple_Check(obj) ||
             PyObject_IsInstance(obj, s->sequence_types))
    {
        // See https://github.com/python/cpython/issues/123593 
        if (PyErr_Occurred())
            return -1;

        if (_Py_EnterRecursiveCall(" while encoding a JSON object"))
            return -1;
        rv = encoder_listencode_sequence(s, markers, writer, obj, indent_level, indent_cache);
        _Py_LeaveRecursiveCall();
        return rv;
    }
    else if (PyDict_Check(obj) || PyObject_IsInstance(obj, s->mapping_types)) {
        if (PyErr_Occurred())
            return -1;

        if (_Py_EnterRecursiveCall(" while encoding a JSON object"))
            return -1;
        rv = encoder_listencode_mapping(s, markers, writer, obj, indent_level, indent_cache);
        _Py_LeaveRecursiveCall();
        return rv;
    }
    else if (PyObject_TypeCheck(obj, (PyTypeObject *)s->Decimal)) {
        PyObject *encoded = encoder_encode_decimal(s, obj);
        if (encoded == NULL)
            return -1;
        return _steal_accumulate(writer, encoded);
    }
    else {
        PyErr_Format(PyExc_TypeError,
                     "%.100s is not JSON serializable", Py_TYPE(obj)->tp_name);
        return -1;
    }
}

static int
encoder_encode_key_value(PyEncoderObject *s, PyObject *markers, _PyUnicodeWriter *writer, bool *first,
                         PyObject *key, PyObject *value,
                         Py_ssize_t indent_level, PyObject *indent_cache,
                         PyObject *item_separator)
{
    PyObject *keystr = NULL;
    PyObject *encoded;

    if (PyUnicode_Check(key) || PyObject_IsInstance(key, s->str_types)) {
        if (PyErr_Occurred())
            return -1;
        keystr = PyObject_Str(key);
        if (keystr == NULL)
            return -1;
    }
    else {
        PyErr_Format(PyExc_TypeError,
                     "Keys must be str, not %.100s", Py_TYPE(key)->tp_name);
        return -1;
    }

    if (keystr == NULL) {
        return -1;
    }

    if (*first) {
        *first = false;
    }
    else {
        if (_PyUnicodeWriter_WriteStr(writer, item_separator) < 0) {
            Py_DECREF(keystr);
            return -1;
        }
    }

    if (!s->quoted_keys && PyUnicode_IsIdentifier(keystr) &&
        (!s->ensure_ascii || PyUnicode_IS_ASCII(key)))
    {
        encoded = keystr;
    }
    else {
        encoded = encoder_encode_string(s, keystr);
        Py_DECREF(keystr);
    }

    if (encoded == NULL) {
        return -1;
    }

    if (_steal_accumulate(writer, encoded) < 0) {
        return -1;
    }
    if (_PyUnicodeWriter_WriteStr(writer, s->key_separator) < 0) {
        return -1;
    }
    if (encoder_listencode_obj(s, markers, writer, value, indent_level, indent_cache) < 0) {
        return -1;
    }
    return 0;
}

static int
encoder_listencode_mapping(PyEncoderObject *s, PyObject *markers, _PyUnicodeWriter *writer,
                           PyObject *mapping,
                           Py_ssize_t indent_level, PyObject *indent_cache)
{
    /* Encode Python mapping to a JSON term */
    PyObject *ident = NULL;
    PyObject *items = NULL;
    PyObject *key, *value;
    bool first = true;

    if (PyMapping_Size(mapping) == 0)  /* Fast path */
        return _PyUnicodeWriter_WriteASCIIString(writer, "{}", 2);

    int has_key;
    ident = PyLong_FromVoidPtr(mapping);
    if (ident == NULL)
        goto bail;
    has_key = PyDict_Contains(markers, ident);
    if (has_key == -1)
    {
        goto bail;
    }
    if (has_key) {
        PyErr_SetString(PyExc_ValueError, "Unexpected circular reference");
        goto bail;
    }
    if (PyDict_SetItem(markers, ident, mapping) < 0) {
        goto bail;
    }

    if (_PyUnicodeWriter_WriteChar(writer, '{') < 0)
        goto bail;

    int indented;
    if (s->indent == Py_None || indent_level >= s->max_indent_level) {
        indented = false;
    }
    else if (s->indent_leaves) {
        indented = true;
    }
    else {
        indented = false;
        PyObject *values = PyMapping_Values(mapping);
        if (values == NULL)
            goto bail;

        for (Py_ssize_t  i = 0; i < PyList_GET_SIZE(values); i++) {
            PyObject *obj = PyList_GET_ITEM(values, i);
            if (PyList_Check(obj) || PyTuple_Check(obj) || PyDict_Check(obj) ||
                PyObject_IsInstance(obj, s->sequence_types) ||
                PyObject_IsInstance(obj, s->mapping_types))
            {
                if (PyErr_Occurred()) {
                    goto bail;
                }
                indented = true;
                break;
            }
        }
        Py_CLEAR(values);
    }

    PyObject *separator;
    if (!indented) {
        separator = s->long_item_separator; // borrowed reference
    }
    else {
#ifdef Py_DEBUG
        assert(s->indent != Py_None);
#endif
        indent_level++;
        separator = get_item_separator(s, indent_level, indent_cache);
        if (separator == NULL ||
            write_newline_indent(writer, indent_level, indent_cache) < 0)
        {
            goto bail;
        }
    }

    if (s->sort_keys || !PyDict_CheckExact(mapping)) {
        items = PyMapping_Items(mapping);
        if (items == NULL || (s->sort_keys && PyList_Sort(items) < 0))
            goto bail;

        for (Py_ssize_t  i = 0; i < PyList_GET_SIZE(items); i++) {
            PyObject *item = PyList_GET_ITEM(items, i);

            if (!PyTuple_Check(item) || PyTuple_GET_SIZE(item) != 2) {
                PyErr_SetString(PyExc_ValueError, "items must return 2-tuples");
                goto bail;
            }

            key = PyTuple_GET_ITEM(item, 0);
            value = PyTuple_GET_ITEM(item, 1);
            if (encoder_encode_key_value(s, markers, writer, &first, key, value,
                                         indent_level, indent_cache,
                                         separator) < 0)
                goto bail;
        }
        Py_CLEAR(items);

    } else {
        Py_ssize_t pos = 0;
        while (PyDict_Next(mapping, &pos, &key, &value)) {
            if (encoder_encode_key_value(s, markers, writer, &first, key, value,
                                         indent_level, indent_cache,
                                         separator) < 0)
                goto bail;
        }
        // PyDict_Next could return an error, we need to handle it
        if (PyErr_Occurred())
            goto bail;
    }

    if (PyDict_DelItem(markers, ident) < 0)
        goto bail;
    Py_CLEAR(ident);
    if (indented) {
        indent_level--;
        if ((s->trailing_comma && _PyUnicodeWriter_WriteStr(writer, s->item_separator) < 0) ||
            write_newline_indent(writer, indent_level, indent_cache) < 0)
        {
            goto bail;
        }
    }

    if (_PyUnicodeWriter_WriteChar(writer, '}') < 0)
        goto bail;
    return 0;

bail:
    Py_XDECREF(items);
    Py_XDECREF(ident);
    return -1;
}

static int
encoder_listencode_sequence(PyEncoderObject *s, PyObject *markers, _PyUnicodeWriter *writer,
                            PyObject *seq,
                            Py_ssize_t indent_level, PyObject *indent_cache)
{
    PyObject *ident = NULL;
    PyObject *s_fast = NULL;
    Py_ssize_t i;

    ident = NULL;
    s_fast = PySequence_Fast(seq, "_iterencode_sequence needs a sequence");
    if (s_fast == NULL)
        return -1;
    if (PySequence_Fast_GET_SIZE(s_fast) == 0) {
        Py_DECREF(s_fast);
        return _PyUnicodeWriter_WriteASCIIString(writer, "[]", 2);
    }

    int has_key;
    ident = PyLong_FromVoidPtr(seq);
    if (ident == NULL)
        goto bail;
    has_key = PyDict_Contains(markers, ident);
    if (has_key == -1)
        goto bail;

    if (has_key) {
        PyErr_SetString(PyExc_ValueError, "Unexpected circular reference");
        goto bail;
    }
    if (PyDict_SetItem(markers, ident, seq) < 0) {
        goto bail;
    }

    if (_PyUnicodeWriter_WriteChar(writer, '[') < 0)
        goto bail;

    int indented;
    if (s->indent == Py_None || indent_level >= s->max_indent_level) {
        indented = false;
    }
    else if (s->indent_leaves) {
        indented = true;
    }
    else {
        indented = false;
        for (i = 0; i < PySequence_Fast_GET_SIZE(s_fast); i++) {
            PyObject *obj = PySequence_Fast_GET_ITEM(s_fast, i);
            if (PyList_Check(obj) || PyTuple_Check(obj) || PyDict_Check(obj) ||
                PyObject_IsInstance(obj, s->sequence_types) ||
                PyObject_IsInstance(obj, s->mapping_types))
            {
                if (PyErr_Occurred()) {
                    goto bail;
                }
                indented = true;
                break;
            }
        }
    }

    PyObject *separator;
    if (!indented) {
        separator = s->long_item_separator; // borrowed reference
    }
    else {
#ifdef Py_DEBUG
        assert(s->indent != Py_None);
#endif
        indent_level++;
        separator = get_item_separator(s, indent_level, indent_cache);
        if (separator == NULL ||
            write_newline_indent(writer, indent_level, indent_cache) < 0)
        {
            goto bail;
        }
    }
    for (i = 0; i < PySequence_Fast_GET_SIZE(s_fast); i++) {
        PyObject *obj = PySequence_Fast_GET_ITEM(s_fast, i);
        if (i) {
            if (_PyUnicodeWriter_WriteStr(writer, separator) < 0)
                goto bail;
        }
        if (encoder_listencode_obj(s, markers, writer, obj, indent_level, indent_cache) < 0)
            goto bail;
    }
    if (PyDict_DelItem(markers, ident) < 0)
        goto bail;
    Py_CLEAR(ident);

    if (indented) {
        indent_level--;
        if ((s->trailing_comma && _PyUnicodeWriter_WriteStr(writer, s->item_separator) < 0) ||
            write_newline_indent(writer, indent_level, indent_cache) < 0)
        {
            goto bail;
        }
    }

    if (_PyUnicodeWriter_WriteChar(writer, ']') < 0)
        goto bail;
    Py_DECREF(s_fast);
    return 0;

bail:
    Py_XDECREF(ident);
    Py_DECREF(s_fast);
    return -1;
}

static void
encoder_dealloc(PyObject *self)
{
    PyTypeObject *tp = Py_TYPE(self);
    /* bpo-31095: UnTrack is needed before calling any callbacks */
    PyObject_GC_UnTrack(self);
    (void)encoder_clear(self);
    tp->tp_free(self);
    Py_DECREF(tp);
}

static int
encoder_traverse(PyObject *op, visitproc visit, void *arg)
{
    PyEncoderObject *self = PyEncoderObject_CAST(op);
    Py_VISIT(Py_TYPE(self));
    Py_VISIT(self->bool_types);
    Py_VISIT(self->float_types);
    Py_VISIT(self->indent);
    Py_VISIT(self->int_types);
    Py_VISIT(self->mapping_types);
    Py_VISIT(self->sequence_types);
    Py_VISIT(self->str_types);
    Py_VISIT(self->end);
    Py_VISIT(self->key_separator);
    Py_VISIT(self->item_separator);
    Py_VISIT(self->long_item_separator);
    return 0;
}

static int
encoder_clear(PyObject *op)
{
    PyEncoderObject *self = PyEncoderObject_CAST(op);
    /* Deallocate Encoder */
    Py_CLEAR(self->bool_types);
    Py_CLEAR(self->float_types);
    Py_CLEAR(self->indent);
    Py_CLEAR(self->int_types);
    Py_CLEAR(self->mapping_types);
    Py_CLEAR(self->sequence_types);
    Py_CLEAR(self->str_types);
    Py_CLEAR(self->end);
    Py_CLEAR(self->key_separator);
    Py_CLEAR(self->item_separator);
    Py_CLEAR(self->long_item_separator);
    return 0;
}

PyDoc_STRVAR(encoder_doc, "Make JSON encoder");

static PyType_Slot PyEncoderType_slots[] = {
    {Py_tp_doc, (void *)encoder_doc},
    {Py_tp_dealloc, encoder_dealloc},
    {Py_tp_call, encoder_call},
    {Py_tp_traverse, encoder_traverse},
    {Py_tp_clear, encoder_clear},
    {Py_tp_new, encoder_new},
    {0, 0}
};

static PyType_Spec PyEncoderType_spec = {
    .name = "_jsonyx.Encoder",
    .basicsize = sizeof(PyEncoderObject),
    .itemsize = 0,
    .flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
    .slots = PyEncoderType_slots
};

PyDoc_STRVAR(module_doc,
"json speedups\n");

static int
_json_exec(PyObject *module)
{
    PyObject *PyScannerType = PyType_FromSpec(&PyScannerType_spec);
    int rc = PyModule_AddObject(module, "make_scanner", PyScannerType);
    if (rc < 0) {
        Py_XDECREF(PyScannerType);
        return -1;
    }

    PyObject *PyEncoderType = PyType_FromSpec(&PyEncoderType_spec);
    rc = PyModule_AddObject(module, "make_encoder", PyEncoderType);
    if (rc < 0) {
        Py_XDECREF(PyEncoderType);
        return -1;
    }

    return 0;
}

static PyModuleDef_Slot _json_slots[] = {
    {Py_mod_exec, _json_exec},
#if defined Py_mod_multiple_interpreters && defined Py_MOD_PER_INTERPRETER_GIL_SUPPORTED
    {Py_mod_multiple_interpreters, Py_MOD_PER_INTERPRETER_GIL_SUPPORTED},
#endif
#if defined Py_mod_gil && defined Py_MOD_GIL_NOT_USED
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
#endif
    {0, NULL}
};

static struct PyModuleDef jsonmodule = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "_jsonyx",
    .m_doc = module_doc,
    .m_slots = _json_slots,
};

PyMODINIT_FUNC
PyInit__jsonyx(void)
{
    return PyModuleDef_Init(&jsonmodule);
}
