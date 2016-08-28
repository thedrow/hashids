# -*- coding: utf-8 -*-

import os

from cffi import FFI
ffi = FFI()

ffi.cdef("""
/* exported hashids_errno */
extern int hashids_errno;

/* the hashids "object" */
struct hashids_t {
    wchar_t *alphabet;
    wchar_t *alphabet_copy_1;
    wchar_t *alphabet_copy_2;
    unsigned int alphabet_length;

    wchar_t *salt;
    unsigned int salt_length;

    wchar_t *separators;
    unsigned int separators_count;

    wchar_t *guards;
    unsigned int guards_count;

    unsigned int min_hash_length;
};

/* exported function definitions */
void
hashids_shuffle(wchar_t *str, int str_length, wchar_t *salt, int salt_length);

void
hashids_free(struct hashids_t *hashids);

struct hashids_t *
hashids_init3(const wchar_t *salt, unsigned int min_hash_length,
    const wchar_t *alphabet);

struct hashids_t *
hashids_init2(const wchar_t *salt, unsigned int min_hash_length);

struct hashids_t *
hashids_init(const wchar_t *salt);

unsigned int
hashids_estimate_encoded_size(struct hashids_t *hashids,
    unsigned int numbers_count, unsigned long long *numbers);

unsigned int
hashids_estimate_encoded_size_v(struct hashids_t *hashids, unsigned int numbers_count, ...);

unsigned int
hashids_encode(struct hashids_t *hashids, wchar_t *buffer,
    unsigned int numbers_count, unsigned long long *numbers);

unsigned int
hashids_encode_v(struct hashids_t *hashids, wchar_t *buffer, unsigned int numbers_count, ...);

unsigned int
hashids_encode_one(struct hashids_t *hashids, wchar_t *buffer,
    unsigned long long number);

unsigned int
hashids_numbers_count(struct hashids_t *hashids, wchar_t *str);

unsigned int
hashids_decode(struct hashids_t *hashids, wchar_t *str,
    unsigned long long *numbers);

unsigned int
hashids_encode_hex(struct hashids_t *hashids, wchar_t *buffer,
    const wchar_t *hex_str);

unsigned int
hashids_decode_hex(struct hashids_t *hashids, wchar_t *str, wchar_t *output);

// CFFI code
void free(void *);

wchar_t *encode_one(struct hashids_t *hashids, unsigned long long number);
wchar_t *encode(struct hashids_t *hashids, unsigned int numbers_count, unsigned long long *numbers);

unsigned long long *decode(struct hashids_t *hashids, wchar_t *str, unsigned int *numbers_count);
""")

vendored_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../vendor/hashids.c')

with open(os.path.join(vendored_path, 'hashids.c')) as f:
    source = f.read()

ffi.set_source('hashids_cffi._hashids',
"""
#include <hashids.h>

%s

wchar_t *encode_one(struct hashids_t *hashids, unsigned long long number) {
    wchar_t *buffer = calloc(hashids_estimate_encoded_size(hashids, 1, &number), 1);
    if (!buffer) {
        return NULL;
    }

    if (hashids_encode_one(hashids, buffer, number) == 0) {
        return NULL;
    }

    return buffer;
}

wchar_t *encode(struct hashids_t *hashids, unsigned int numbers_count, unsigned long long *numbers)
{
    wchar_t *buffer = calloc(hashids_estimate_encoded_size(hashids, numbers_count, numbers), 1);
    if (!buffer) {
        return NULL;
    }

    if (hashids_encode(hashids, buffer, numbers_count, numbers) == 0) {
        return NULL;
    }

    return buffer;
}

unsigned long long *decode(struct hashids_t *hashids, wchar_t *str, unsigned int *numbers_count) {
    *numbers_count = hashids_numbers_count(hashids, str);

    if (!*numbers_count) {
        return NULL;
    }

    unsigned long long *numbers = calloc(*numbers_count, sizeof(unsigned long long));

    if (!numbers) {
        return NULL;
    }

    if (!hashids_decode(hashids, str, numbers)) {
        return NULL;
    }

    return numbers;
}
""" % source,
include_dirs=[vendored_path])

if __name__ == "__main__":
    ffi.compile()
