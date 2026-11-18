"""Subtítulos del montaje (HAL-04 de la auditoría de PAL-2026-001) y geometría del Stomachion."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import montaje  # noqa: E402


class TestSubtitulos(unittest.TestCase):
    def test_no_parte_tras_iniciales(self):
        texto = "1906, Constantinopla. El filólogo J. L. Heiberg examina un libro de oraciones y advierte algo."
        for _, _, x in montaje.cues(texto, 0, 10):
            self.assertFalse(x.endswith(("J.", "L.")), x)
            for linea in montaje.partir(x, 42).split("\n"):
                self.assertFalse(linea.endswith(("J.", "L.")), linea)

    def test_sin_subtitulos_de_menos_de_un_segundo(self):
        texto = "Así que la pregunta no es si este libro es valioso. Lo es. La pregunta es otra: ¿cuánto?"
        for a, b, _ in montaje.cues(texto, 0, 9):
            self.assertGreaterEqual(b - a, 1.0)

    def test_lineas_de_42(self):
        texto = "Si se cuentan además las simetrías del cuadrado y el intercambio de piezas iguales, son 17.152."
        for _, _, x in montaje.cues(texto, 0, 8, 76):
            self.assertTrue(all(len(l) <= 42 for l in montaje.partir(x, 42).split("\n")))


class TestStomachion(unittest.TestCase):
    def test_14_piezas_y_area_144(self):
        area = lambda p: abs(sum(p[i][0] * p[i - 1][1] - p[i - 1][0] * p[i][1] for i in range(len(p)))) / 2
        self.assertEqual(len(montaje.STOMACHION), 14)
        self.assertEqual(sum(area(p) for p in montaje.STOMACHION), 144)
        self.assertEqual(sorted(area(p) for p in montaje.STOMACHION), [3, 3, 6, 6, 6, 6, 9, 12, 12, 12, 12, 12, 21, 24])


if __name__ == "__main__":
    unittest.main()
