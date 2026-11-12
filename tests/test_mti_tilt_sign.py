"""Check the manuscript's MTI tilt convention without fitting a model.

Run with: python3 -m unittest discover -s tests -v
"""

from fractions import Fraction
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MIDPOINT = r"\rho_c\{(y-m)^2-h^2\}-2c\delta(m-y)"
REVERSED_MIDPOINT = r"\rho_c\{(y-m)^2-h^2\}-2c\delta(y-m)"
ROOT_FORM = r"\rho_c(e_i)-c\delta_i(\eta_{1i}+\eta_{2i}-2y_i)"
POSITIVE_SHIFT = r"=h_1+\omega_{\mathrm R}c\mat X^\top\delta"


def compact(text):
    return "".join(text.split())


def check_source_convention(main, supplement):
    main, supplement = compact(main), compact(supplement)
    if REVERSED_MIDPOINT in main:
        raise ValueError("The midpoint tilt has the reversed sign.")
    for expression, text in (
        (MIDPOINT, main),
        (ROOT_FORM, supplement),
        (POSITIVE_SHIFT, main),
        (r"\mu+\delta", main),
    ):
        if compact(expression) not in text:
            raise ValueError("Missing MTI sign convention: " + expression)


def check_loss(residual, content):
    return residual * (content - int(residual < 0))


class TiltSignTests(unittest.TestCase):
    def test_manuscripts_use_one_tilt_convention(self):
        check_source_convention(
            (ROOT / "main.tex").read_text(encoding="utf-8"),
            (ROOT / "mti-extensions-supplement.tex").read_text(encoding="utf-8"),
        )

    def test_reversed_midpoint_expression_is_rejected(self):
        main = MIDPOINT + POSITIVE_SHIFT + r"\mu+\delta"
        check_source_convention(main, ROOT_FORM)
        with self.assertRaisesRegex(ValueError, "reversed sign"):
            check_source_convention(main.replace(MIDPOINT, REVERSED_MIDPOINT), ROOT_FORM)

    def test_midpoint_and_root_losses_are_identical(self):
        for content in (0.2, 0.5, 0.9):
            for tilt in (-0.7, 0.0, 0.7):
                for y in (-3.0, 0.25, 4.0):
                    midpoint, halfwidth = 0.3, 1.2
                    lower, upper = midpoint - halfwidth, midpoint + halfwidth
                    root_loss = check_loss((y - lower) * (y - upper), content)
                    root_loss -= content * tilt * (lower + upper - 2 * y)
                    midpoint_loss = check_loss((y - midpoint) ** 2 - halfwidth**2, content)
                    midpoint_loss -= 2 * content * tilt * (midpoint - y)
                    self.assertAlmostEqual(root_loss, midpoint_loss, places=12)

    def test_stationary_scores_imply_retained_mean_plus_tilt(self):
        # An exact four-point example, with no probability mass at either root.
        content = Fraction(4, 5)
        probabilities = (Fraction(1, 10), Fraction(2, 5), Fraction(2, 5), Fraction(1, 10))
        lower, upper = Fraction(-2), Fraction(2)
        for reflection in (-1, 1):
            values = tuple(Fraction(reflection * y) for y in (-6, -1, 1, 4))
            mean = sum(p * y for p, y in zip(probabilities, values))
            retained = sum(p * y for p, y in zip(probabilities, values) if lower < y < upper)
            tilt = retained / content - mean
            scores = tuple(content - int(lower < y < upper) for y in values)
            first = sum(p * s * (upper - y) for p, s, y in zip(probabilities, scores, values))
            second = sum(p * s * (lower - y) for p, s, y in zip(probabilities, scores, values))
            self.assertEqual(first - content * tilt, 0)
            self.assertEqual(second - content * tilt, 0)
            self.assertEqual(retained / content, mean + tilt)
            self.assertNotEqual(retained / content, mean - tilt)
            self.assertNotEqual(first + content * tilt, 0)

    def test_positive_canonical_shift_matches_both_gaussian_root_kernels(self):
        values, latent = (-1.0, 0.25, 1.5, 3.0), (0.4, 0.5, 0.3, 0.8)
        omega, prior_precision = 1.3, 0.01
        sigma = 1 / omega
        for content in (0.2, 0.5, 0.9):
            xi = (1 - 2 * content) / (content * (1 - content))
            phi = 2 / (content * (1 - content))
            for tilt in (-0.2, 0.0, 0.2):
                def kernel(first, second):
                    result = -sum(
                        ((y - first) * (y - second) - xi * v) ** 2 / (2 * phi * sigma * v)
                        for y, v in zip(values, latent)
                    )
                    result += omega * len(values) * content * tilt * (first + second)
                    return result - prior_precision * (first**2 + second**2) / 2

                other = 2.0
                precision = prior_precision + sum(
                    (y - other) ** 2 / (phi * sigma * v) for y, v in zip(values, latent)
                )
                information = sum(
                    (y - other) * (y * (y - other) - xi * v) / (phi * sigma * v)
                    for y, v in zip(values, latent)
                ) + omega * len(values) * content * tilt
                for root in (-2.0, -0.1, 0.8):
                    expected = information * root - precision * root**2 / 2
                    self.assertAlmostEqual(kernel(root, other) - kernel(0, other), expected, places=10)
                    self.assertAlmostEqual(kernel(other, root) - kernel(other, 0), expected, places=10)


if __name__ == "__main__":
    unittest.main()
