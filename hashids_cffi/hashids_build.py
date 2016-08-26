# -*- coding: utf-8 -*-

import os

from cffi import FFI
ffi = FFI()

ffi.cdef("""
/* exported hashids_errno */
extern int hashids_errno;

/* the hashids "object" */
struct hashids_t {
    char *alphabet;
    char *alphabet_copy_1;
    char *alphabet_copy_2;
    unsigned int alphabet_length;

    char *salt;
    unsigned int salt_length;

    char *separators;
    unsigned int separators_count;

    char *guards;
    unsigned int guards_count;

    unsigned int min_hash_length;
};

/* exported function definitions */
void
hashids_shuffle(char *str, int str_length, char *salt, int salt_length);

void
hashids_free(struct hashids_t *hashids);

struct hashids_t *
hashids_init3(const char *salt, unsigned int min_hash_length,
    const char *alphabet);

struct hashids_t *
hashids_init2(const char *salt, unsigned int min_hash_length);

struct hashids_t *
hashids_init(const char *salt);

unsigned int
hashids_estimate_encoded_size(struct hashids_t *hashids,
    unsigned int numbers_count, unsigned long long *numbers);

unsigned int
hashids_estimate_encoded_size_v(struct hashids_t *hashids, unsigned int numbers_count, ...);

unsigned int
hashids_encode(struct hashids_t *hashids, char *buffer,
    unsigned int numbers_count, unsigned long long *numbers);

unsigned int
hashids_encode_v(struct hashids_t *hashids, char *buffer, unsigned int numbers_count, ...);

unsigned int
hashids_encode_one(struct hashids_t *hashids, char *buffer,
    unsigned long long number);

unsigned int
hashids_numbers_count(struct hashids_t *hashids, char *str);

unsigned int
hashids_decode(struct hashids_t *hashids, char *str,
    unsigned long long *numbers);

unsigned int
hashids_encode_hex(struct hashids_t *hashids, char *buffer,
    const char *hex_str);

unsigned int
hashids_decode_hex(struct hashids_t *hashids, char *str, char *output);

// CFFI code
void free(void *);

char *encode_one(struct hashids_t *hashids, unsigned long long number);
char *encode(struct hashids_t *hashids, unsigned int numbers_count, unsigned long long *numbers);
char *encode_hex(struct hashids_t *hashids, const char *hex_str);

unsigned long long *decode(struct hashids_t *hashids, char *str, unsigned int *numbers_count);
""")

vendored_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../vendor/hashids.c')

with open(os.path.join(vendored_path, 'hashids.c')) as f:
    source = f.read()

ffi.set_source('hashids_cffi._hashids',
"""
#include <hashids.h>

%s

char *encode_one(struct hashids_t *hashids, unsigned long long number) {
    char *buffer = calloc(hashids_estimate_encoded_size(hashids, 1, &number), 1);
    if (!buffer) {
        return NULL;
    }

    if (hashids_encode_one(hashids, buffer, number) == 0) {
        return NULL;
    }

    return buffer;
}

char *encode(struct hashids_t *hashids, unsigned int numbers_count, unsigned long long *numbers)
{
    char *buffer = calloc(hashids_estimate_encoded_size(hashids, numbers_count, numbers), 1);
    if (!buffer) {
        return NULL;
    }

    if (hashids_encode(hashids, buffer, numbers_count, numbers) == 0) {
        return NULL;
    }

    return buffer;
}

char *encode_hex(struct hashids_t *hashids, const char *hex_str) {
    unsigned long long number = (unsigned long long)-1;
    char *buffer = calloc(hashids_estimate_encoded_size(hashids, 1, &number), 1);

    if (!buffer) {
        return NULL;
    }

    hashids_encode_hex(hashids, buffer, hex_str);

    return buffer;
}

unsigned long long *decode(struct hashids_t *hashids, char *str, unsigned int *numbers_count) {
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
