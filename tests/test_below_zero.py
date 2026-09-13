#!/usr/bin/env python3
"""Tests for the Below Zero pandas assignment."""

import contextlib
import io
import os
import unittest
from unittest.mock import patch

import pandas as pd

from src.below_zero import below_zero, main


class TestBelowZero(unittest.TestCase):
    """below_zero() -> count of days below zero in kumpula-weather-2017.csv."""

    def test_value(self):
        result = below_zero()
        self.assertEqual(
            result,
            49,
            msg="below_zero() should return 49: the number of days in "
            "kumpula-weather-2017.csv whose mean temperature is below zero.",
        )

    def test_output(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main()
        out = buf.getvalue()
        pattern = r"Number of days below zero:\s+\d+"
        self.assertRegex(
            out,
            pattern,
            msg="main() should print a line like 'Number of days below zero: "
            "49'. Got: %r" % (out,),
        )

    def test_main_reads_the_expected_csv_via_below_zero(self):
        with patch("src.below_zero.below_zero", wraps=below_zero) as pbz, patch(
            "src.below_zero.pd.read_csv", wraps=pd.read_csv
        ) as prc:
            main()
            pbz.assert_called_once()
            prc.assert_called_once()
            args, kwargs = prc.call_args
            self.assertEqual(
                os.path.basename(args[0]),
                "kumpula-weather-2017.csv",
                msg="below_zero() should read 'kumpula-weather-2017.csv', not "
                "a different file.",
            )
            if "sep" in kwargs:
                self.assertEqual(
                    kwargs["sep"],
                    ",",
                    msg="If a sep argument is given to read_csv, it should be "
                    "',' since the file is comma-separated.",
                )


if __name__ == "__main__":
    unittest.main()
