# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import numpy

import awkward as ak


def to_numpy(array, *, allow_missing=True):
    """
    Args:
        array: Array-like data (anything #ak.to_layout recognizes).
        allow_missing (bool): allow missing (None) values.

    Converts `array` (many types supported, including all Awkward Arrays and
    Records) into a NumPy array, if possible.

    If the data are numerical and regular (nested lists have equal lengths
    in each dimension, as described by the #ak.Array.type), they can be losslessly
    converted to a NumPy array and this function returns without an error.

    Otherwise, the function raises an error. It does not create a NumPy
    array with dtype `"O"` for `np.object_` (see the
    [note on object_ type](https://docs.scipy.org/doc/numpy/reference/arrays.scalars.html#arrays-scalars-built-in))
    since silent conversions to dtype `"O"` arrays would not only be a
    significant performance hit, but would also break functionality, since
    nested lists in a NumPy `"O"` array are severed from the array and
    cannot be sliced as dimensions.

    If `array` is not an Awkward Array, then this function is equivalent
    to calling `np.asarray` on it.

    If `allow_missing` is True; NumPy
    [masked arrays](https://docs.scipy.org/doc/numpy/reference/maskedarray.html)
    are a possible result; otherwise, missing values (None) cause this
    function to raise an error.

    See also #ak.from_numpy and #ak.to_cupy.
    """
    with ak._errors.OperationErrorContext(
        "ak.to_numpy",
        dict(array=array, allow_missing=allow_missing),
    ):
        with numpy.errstate(invalid="ignore"):
            return ak._util.to_arraylib(numpy, array, allow_missing)
