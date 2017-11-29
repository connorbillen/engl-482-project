#!/usr/bin/python3

import string
from difflib import SequenceMatcher
from FAVEToTxt import Letter, Word

# similarity ratio used to determine if two things are probably "the same"
CLOSE_ENOUGH = 0.6

# useful difflib functions:
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

    blob_matcher = SequenceMatcher(junk_func)
    word_matcher.set_seq2(common_text)
    word_matcher.set_seq1(vary_text)

    # overall ratio which considers slightly different words to be totally different
    print("Overall text blob ratio: {}".format(blob_matcher.ratio()));
    print("Word-by-word ratio: {}".format(word_matcher.ratio()));

    nwords = len(common_text_words)
    char_matcher = SequenceMatcher(junk_func)
    for i in range(0, nwords):
        print("== {} -> {} ==".format(common_text_words[i], vary_text_words[i]))
        char_matcher.set_seqs(common_text_words[i], vary_text_words[i])
        print("   Similarity: {:.1%}".format(round(char_matcher.ratio(), 3)))
        for tag, a1, a2, b1, b2 in char_matcher.get_opcodes():
            # only print differences
            if tag == 'equal':
                continue
            # longest opcode is "replace" (7 characters)
            print("   {:7}   a[{}:{}] -> b[{}:{}]   {!r} -> {!r}".format(
                tag, a1, a2, b1, b2, common_text_words[i][a1:a2], vary_text_words[i][b1:b2]))

# gets word-by-word opcodes for a transcription
def getOpcodes(standard_words, regional_words):
    junk_func = lambda x: x.isspace()
    word_matcher = SequenceMatcher(junk_func)

    opcodes = []
    for (standard_word, regional_word) in zip(standard_words, regional_words):
        standard_letters = [letter.char for letter in standard_word.letters]
        regional_letters = [letter.char for letter in regional_word.letters]
        word_matcher.set_seq1(standard_letters)
        word_matcher.set_seq2(regional_letters)
        opcodes.append(word_matcher.get_opcodes())
        # similarity factor: word_matcher.ratio()

    return opcodes;

# gets a list of the indices of words that differ
def getDifferentWordIndices(standard_words, regional_words):
    diff_indices = []
    for index, (standard_word, regional_word) in enumerate(zip(standard_words, regional_words)):
        standard_letters = [letter.char for letter in standard_word.letters]
        regional_letters = [letter.char for letter in regional_word.letters]
        if standard_letters != regional_letters:
            diff_indices.append(index)

    return diff_indices
