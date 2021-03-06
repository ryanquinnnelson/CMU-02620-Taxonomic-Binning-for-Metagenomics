"""
Defines encoding functionality for metagenomics data generated using the sampling module.
Grouping of data into kmers is performed using single loop and non-vectorized operations.
"""
import numpy as np
import math
from sklearn.preprocessing import OneHotEncoder


# tested
def _split_into_kmers(fragment, k):
    """
    Subdivides fragment into k elements, starting from the first position. Discards partial fragments.
    Total number of elements produced is T = floor(L/k) where L is the fragment length

    :param fragment: fragment to be split
    :param k: size of elements fragment should be split into
    :return: T x 1 array, where T is the number of elements produced by the split
    """
    # decode binary string
    decoded = fragment.decode('utf-8')
    dtype = '|S' + str(k)

    # split into k-mers
    # source: https://stackoverflow.com/questions/22571259/split-a-string-into-n-equal-parts
    k_mers = np.array(list(map(''.join, zip(*[iter(decoded)] * k))), dtype=dtype)
    return k_mers


# tested
def _generate_kmers(fragments, k):
    """
    Converts fragments dataset into dataset of k-mers.

    Todo - needs to be parallelized or sped up in some way

    :param fragments: fragment to be split
    :param k: size of elements fragment should be split into
    :return: n x T matrix, where n is the number of fragments and T is the number of elements produced by the split
    """
    n_frag = len(fragments)  # number of rows
    sample_length = len(fragments[0])
    n_kmers = math.floor(sample_length / k)  # number of k-mers per row

    # process fragments
    kmers = np.chararray((n_frag, n_kmers), itemsize=k)
    for i, val in enumerate(fragments):
        row = _split_into_kmers(val, k)
        kmers[i] = row

    return kmers


# tested
def encode_fragment_dataset(fragments, k):
    """
    Converts fragments into k-mers and encodes the data using one-hot encoding.

    Todo - Determine best time to convert binary string to string. Do I leave data as string

    :param fragments: fragment to be split
    :param k: size of elements fragment should be split into
    :return: sparse matrix
    """

    # generate k_mers
    X = _generate_kmers(fragments, k)
    X = X.astype('str')  # convert binary string data type to string

    # encode data using one-hot encoding
    return OneHotEncoder().fit_transform(X)
