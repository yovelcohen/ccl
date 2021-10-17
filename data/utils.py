import scipy.stats
import numpy as np
import logging

logger = logging.getLogger(__file__)


def normalize_event_histogram(results, feat_names, total_events_count):
    """
    this function normalizes the event's histogram, we want to sharpen time gaps between events
    so when we zoom the algorithm in later on certain period.
    """
    lists = {feat: [] for feat in feat_names}
    trans = {}
    stds = {}
    for feat_name, l in list(lists.items()):
        l.extend([0] * (total_events_count - len(l)))
        h, _ = np.histogram(l, bins=[0.1 * i for i in range(11)])
        # add the feature's standard deviation
        stds[feat_name] = np.std(l)
        nonzeros = sum(1 for val in l if val)
        mx = max(l)
        mn = min(l)
        logger.info("Histogram of feature", extra={'feature_name': feat_names[feat_name],
                                                   'full_elements': nonzeros,
                                                   'max_element': mx,
                                                   'histogram': h})
        vals = sorted(l)

        # exponential growth in event & feature combo over time,
        # might be useful later in comparison to the feature relation in other events? idkkk
        _map = {
            val:
                scipy.stats.expon.ppf(0.999) if val > 0 and val == mx
            else 0 if val == mn
            else scipy.stats.expon.ppf(0.999 * i / len(vals))
            for i, val in enumerate(vals)
        }
        trans[feat_name] = _map

    for event_id, features in list(results.items()):
        for feat_name in feat_names:
            if feat_name not in features:
                continue
            orig = features[feat_name]['raw']
            features[feat_name]['final'] = trans[feat_name][orig]
    return stds
