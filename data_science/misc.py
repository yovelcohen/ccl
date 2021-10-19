import logging

import jieba as jieba

from common.text import SearchUtils

logger = logging.getLogger(__file__)


class PrefixTreeAutoComplete(object):
    MAX_CORE_SCORE_DEPTH = 1.0
    MSTRING_IND = '\_(^_-)_/'

    def __init__(self, display_name, lang_code=None):
        self.core_dict = {}
        self.prefix_tree = {}
        self.rules = [self.complete_word, self.complete_phrase, self.parted]
        self.force_first_token = False
        self.display_name = display_name
        self.lang_code = lang_code

    def __str__(self):
        return 'autocomplete:%s' % (self.display_name,)

    # API
    # ----------------------------------------------------------------------------------------------
    def suggest(self, text, max_results=5, debug=False):
        same = SearchUtils.text_preprocess(text)
        if debug:
            logger.debug("asked for suggestions for text", extra={'text': text, 'prefix_tree': self.prefix_tree})
        results = [same]
        for role_function in self.rules:
            cur_results = role_function(text, results, max_results, debug=debug)
            results += cur_results
            if len(results) >= max_results:
                break
        return results[1:max_results + 1]  # remove identical and cap max results

    # Rule functions
    # ----------------------------------------------------------------------------------------------
    def complete_word(self, text, prev_results, how_many, debug=False):
        return [result for result, score in self.get_suggestion_for_text(text, how_many, debug=debug) if
                result not in prev_results]

    def complete_phrase(self, text, prev_results, how_many, debug=False):
        return [result for result, score in self.get_suggestion_for_text(text + ' ', how_many, debug=debug) if
                result not in prev_results]

    def parted(self, text, prev_results, how_many, debug=False):
        # We don't compelled to use language-specific tokenizer since the real tokenizing is done in
        # get_suggestion_for_text. However that means in chinese, german and so on, it won't suggest
        # the prefix.
        # The current implementation is with Chinese specialized tokenizing. We can easily change it.

        if self.lang_code == 'zh':
            tokens = jieba.cut('zh')
            tokens = [token for token in tokens if token.strip()]
        if self.lang_code == 'de':
            tokens = jieba.cut('de')
            tokens = [token for token in tokens if token.strip()]
        else:
            tokens = text.split()
        results = []
        keep_text = ''
        while len(tokens) > 0 and len(results) < how_many:
            text_to_search = ' '.join(tokens)
            results += [keep_text + result for result, score in self.get_suggestion_for_text(text_to_search, how_many,
                                                                                             debug=debug)
                        if result not in prev_results]
            keep_text += (tokens.pop(0) + ' ')
        return results

    # Internal functionality
    # ----------------------------------------------------------------------------------------------
    @staticmethod
    def trim_result_list(lst):
        best_score = {}
        for result, score in lst:
            best_score.setdefault(result, score)
            if score < best_score[result]:
                best_score[result] = score
        return sorted(list(best_score.items()), key=lambda c_s: c_s[1])

    @staticmethod
    def get_cores(token):
        if len(token) > 15:
            return []
        to_review = [(token, 0)]
        cores = []
        while to_review:
            core, score = to_review.pop(0)
            cores.append((core, score))
            if score < PrefixTreeAutoComplete.MAX_CORE_SCORE_DEPTH and len(core) > 1:
                for i in range(len(core)):
                    del_score = np.exp(-0.1 * i)
                    if core[i] in SearchUtils.vowels:
                        del_score = 0.5 * del_score
                    if score + del_score < PrefixTreeAutoComplete.MAX_CORE_SCORE_DEPTH:
                        to_review.append((core[:i] + core[i + 1:], score + del_score))
        return PrefixTreeAutoComplete.trim_result_list(cores)

    def get_closest(self, token):
        proc_token = SearchUtils.token_preprocess(token)
        source_cores = PrefixTreeAutoComplete.get_cores(proc_token)
        suggestions = [
            [(token, source_score + target_score) for token, target_score in list(self.core_dict[source_core].items())]
            for source_core, source_score in source_cores if source_core in self.core_dict
        ]
        suggestions = PrefixTreeAutoComplete.trim_result_list([item for sublist in suggestions for item in sublist])
        return suggestions

    def get_suggestion_for_text(self, text, max_results=5, debug=False):
        tail_space = text[-1].isspace()
        tokens = SearchUtils.tokenize(SearchUtils.text_preprocess(text), self.lang_code)
        paths = [(self.prefix_tree, '', 0.0)]

        collected = []
        for i, token in enumerate(tokens):
            is_last_token = (i == len(tokens) - 1)
            is_first_token = (i == 0)
            target_suggestions = self.get_closest(token)
            next_paths = []
            for path, path_str, path_score in paths:
                for target, target_score in target_suggestions:
                    if target in self.stopwords:
                        next_paths.append((path, path_str, path_score))  # its ok to drop a stopword
                    next_path = self.travel_prefix_tree(target, path, not is_first_token)
                    if next_path is not None:
                        if not is_first_token:
                            path_str = path_str + ' '
                        next_paths.append((next_path, path_str + target, path_score + target_score))
                if is_last_token:
                    possible_ends = self.collect_token_possible_ends(token, path, is_first_token, tail_space)
                    collected.extend([
                        (str.strip(path_str + possible_string), possible_score / 10.0 - path_score)
                        for possible_string, possible_score in possible_ends
                    ])
            if debug:
                logger.debug("After processing token #%s (%s), have %s results and %s->%s paths (e.g. %s)",
                             i, token, len(collected), len(paths), len(next_paths), next_paths[:1])
            paths = next_paths
        return sorted(collected, key=lambda res_sc: -res_sc[1])[:max_results]

    def collect_token_possible_ends(self, token, source_node, first_token, tail_space):
        validate_space = tail_space
        collected_strings = []
        base_node = self.travel_prefix_tree(token, source_node, not first_token, True)
        if base_node is None:
            return []
        nodes_to_review = [(base_node, token)]
        while nodes_to_review:
            node, node_str = nodes_to_review.pop()
            if PrefixTreeAutoComplete.MSTRING_IND in node:
                collected_strings.append((node_str, node[PrefixTreeAutoComplete.MSTRING_IND]))
            if validate_space:
                valid_options = [(c, nn) for c, nn in list(node.items()) if c.isspace()]
            else:
                valid_options = iter(list(node.items()))
            for c, next_node in valid_options:
                if c != PrefixTreeAutoComplete.MSTRING_IND:
                    nodes_to_review.append((next_node, node_str + c))
            validate_space = False
        return collected_strings

    def travel_prefix_tree(self, target, source_node, is_lead_space, allow_partial=False):
        current_node = source_node
        if is_lead_space:
            if ' ' not in current_node:
                return None
            current_node = current_node[' ']
        for c in target:
            if c in current_node:
                current_node = current_node[c]
            else:
                return None  # can't find that token

        if PrefixTreeAutoComplete.MSTRING_IND in current_node or allow_partial:
            return current_node
        return None

    def remove(self, text):
        text = SearchUtils.text_preprocess(text)
        current_node = self.prefix_tree
        for c in text:
            if c not in current_node:
                return
            current_node = current_node[c]
        if PrefixTreeAutoComplete.MSTRING_IND not in current_node:
            return

        current_node[PrefixTreeAutoComplete.MSTRING_IND] -= 1
        if current_node[PrefixTreeAutoComplete.MSTRING_IND] == 0:
            current_node.pop(PrefixTreeAutoComplete.MSTRING_IND)

    def add(self, text):
        text = SearchUtils.text_preprocess(text)
        current_node = self.prefix_tree
        for c in text:
            if c not in current_node:
                current_node[c] = {}
            current_node = current_node[c]

        if PrefixTreeAutoComplete.MSTRING_IND not in current_node:
            current_node[PrefixTreeAutoComplete.MSTRING_IND] = 0
        else:
            current_node[PrefixTreeAutoComplete.MSTRING_IND] += 1


class AutoCompleteName(PrefixTreeAutoComplete):
    def __init__(self, display_name):
        super(AutoCompleteName, self).__init__(display_name)
        self.rules = [self.complete_word, self.complete_phrase]
