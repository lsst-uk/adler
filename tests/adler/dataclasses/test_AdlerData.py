from numpy.testing import assert_array_equal
import pytest


def test_populate_phase_parameters():
    from adler.dataclasses.AdlerData import AdlerData

    test_object = AdlerData(["u", "g", "r"])

    test_object.populate_phase_parameters("u", "model_1", 11.0, 12.0, 13, 14.0, 15.0, 16.0, 17.0, 18.0)
    test_object.populate_phase_parameters(
        "u", "model_2", 21.0, 22.0, 23, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0
    )
    test_object.populate_phase_parameters("g", "model_1", 31.0, 32.0, 33, 34.0, 35.0, 36.0, 37.0, 38.0)
    test_object.populate_phase_parameters(
        "r", "model_2", 41.0, 42.0, 43, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0
    )

    assert test_object.filter_list == ["u", "g", "r"]
    assert test_object.model_lists == [["model_1", "model_2"], ["model_1"], ["model_2"]]

    assert_array_equal(test_object.phaseAngle_min_adler, [21.0, 31.0, 41.0])
    assert_array_equal(test_object.phaseAngle_range_adler, [22.0, 32.0, 42.0])
    assert_array_equal(test_object.nobs_adler, [23, 33, 43])
    assert_array_equal(test_object.arc_adler, [24.0, 34.0, 44.0])

    # test to make sure the object is correctly populated
    assert test_object.H_adler == [[15.0, 25.0], [35.0], [45.0]]
    assert test_object.H_err_adler == [[16.0, 26.0], [36.0], [46.0]]
    assert test_object.phase_parameter_1 == [[17.0, 27.0], [37.0], [47.0]]
    assert test_object.phase_parameter_1_err == [[18.0, 28.0], [38.0], [48.0]]
    assert test_object.phase_parameter_2 == [[None, 29.0], [None], [49.0]]
    assert test_object.phase_parameter_2_err == [[None, 30.0], [None], [50.0]]

    # testing to make sure the correct error messages trigger
    with pytest.raises(Exception) as error_info_1:
        test_object.populate_phase_parameters(
            "u", "model_1", 11.0, 12.0, 13, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0
        )

    assert (
        error_info_1.value.args[0]
        == "If using a model with 2 phase parameters, both parameter_2 and parameter_2_err must be supplied."
    )

    with pytest.raises(Exception) as error_info_2:
        test_object.populate_phase_parameters("y", "model_1", 11.0, 12.0, 13, 14.0, 15.0, 16.0, 17.0, 18.0)

    assert error_info_2.value.args[0] == "Filter y is not in supplied filter list."