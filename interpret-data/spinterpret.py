#!/usr/bin/python3

import string
from difflib import SequenceMatcher, get_close_matches

# similarity ratio used to determine if two things are probably "the same"
CLOSE_ENOUGH = 0.6

# useful difflib functions:
# get_close_matches -> finds all elements in a list that are "similar" to a value
# SequenceMatcher.ratio -> measures how similar two sequences are as a float in [0, 1]
#   rule of thumb: ratio over .6 is close
# SequenceMatcher.get_matching_blocks -> get matching subsequences between two values


if __name__ == "__main__":
    with open('sample/text1.txt') as f:
        lines = f.readlines()
    # nothing to compare with less than 2 lines
    assert len(lines) >= 2

    # SequenceMatcher is set up to cache one of its comparing sequences ("common sequence").
    # When comparing one sequence against many others, the one sequence should be set as seq2
    common_text = lines[0]
    common_text_words = common_text.split()
    vary_text = lines[1]
    vary_text_words = vary_text.split()

    # make sure word count is the same
    assert len(common_text_words) == len(vary_text_words)

    junk_func = lambda x: x.isspace()

    word_matcher = SequenceMatcher(junk_func)
    word_matcher.set_seq2(common_text_words)
    word_matcher.set_seq1(vary_text_words)

    # overall ratio which considers slightly different words to be totally different
    print("Overall ratio: {}".format(word_matcher.ratio()))

    nwords = len(common_text_words)
    char_matcher = SequenceMatcher(junk_func)
    for i in range(0, nwords):
        print("== {} -> {} ==".format(common_text_words[i], vary_text_words[i]))
        char_matcher.set_seqs(common_text_words[i], vary_text_words[i])
        for tag, a1, a2, b1, b2 in char_matcher.get_opcodes():
            # only print differences
            if tag == 'equal':
                continue
            # longest opcode is "replace" (7 characters)
            print("{:7}   a[{}:{}] -> b[{}:{}]   {!r} -> {!r}".format(
                tag, a1, a2, b1, b2, common_text_words[i][a1:a2], vary_text_words[i][b1:b2]))
