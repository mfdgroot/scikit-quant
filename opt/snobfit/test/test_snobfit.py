import py, os, sys
import numpy as np

sys.path = [os.path.join(os.pardir, 'python')] + sys.path


class TestSNOBFIT:
    def setup_class(cls):
        import SQSnobFit, logging, numpy
        SQSnobFit.log.setLevel(logging.DEBUG)

    def setup_method(self, method):
        import SQSnobFit, numpy

        # reset the random state for each method to get predictable results
        SQSnobFit._gen_utils._randstate = numpy.random.RandomState(6)

    def test01_simple_example(self):
        """Read access to instance public data and verify values"""

        import SQSnobFit

        def f_easy(x):
            from math import sin

            fv = np.inner(x, x)
            fv *= 1 + 0.1*sin(10*(x[0]+x[1]))

            return fv

        bounds = np.array([[-1, 1], [-1, 1]], dtype=float)
        budget = 40
        x0 = np.array([0.5, 0.5])

        res, histout, complete_history = SQSnobFit.minimize(f_easy, x0, bounds, budget)

        # this problem is symmetric, so values may have switched; for
        # simplicity, just check the sum
        assert np.round(sum(res.optpar)-sum((-0.0001, -0.00018)), 8) == 0
        #assert len(histout) == 10
        #assert np.round(histout[9,5:7].sum()-sum((-6.81757191e-03, 8.80742809e-03)), 8) == 0

    def test02_bra(self):
        """Minimize Branin's function"""

        import SQSnobFit

        def bra(x):
            from math import cos, pi

            a = 1
            b = 5.1/(4*pi*pi)
            c = 5/pi
            d = 6
            h = 10
            ff = 1/(8*pi)

            return a*(x[1]-b*x[0]**2+c*x[0]-d)**2+h*(1-ff)*cos(x[0])+h

        bounds = np.array([[-5, 5], [-5, 5]], dtype=float)
        budget = 80      # larger budget needed for full convergence
        x0 = np.array([0.5, 0.5])

        res, histout, complete_history = SQSnobFit.minimize(bra, x0, bounds, budget)
        # LIMIT:
        # fglob = 0.397887357729739
        # xglob = [3.14159265, 2.27500000]
        assert np.round(sum(res.optpar)-sum((3.1416, 2.275)), 8) == 0

    def test03_Hartman6(self):
        """Minimize Hartman6 function"""

        import SQSnobFit

        def Hartman6(x):
            import numpy, math

            a = numpy.array(
                [[10.00,  0.05,  3.00, 17.00],
                 [ 3.00, 10.00,  3.50,  8.00],
                 [17.00, 17.00,  1.70,  0.05],
                 [ 3.50,  0.10, 10.00, 10.00],
                 [ 1.70,  8.00, 17.00,  0.10],
                 [ 8.00, 14.00,  8.00, 14.00]])

            p = numpy.array(
                [[0.1312, 0.2329, 0.2348, 0.4047],
                 [0.1696, 0.4135, 0.1451, 0.8828],
                 [0.5569, 0.8307, 0.3522, 0.8732],
                 [0.0124, 0.3736, 0.2883, 0.5743],
                 [0.8283, 0.1004, 0.3047, 0.1091],
                 [0.5886, 0.9991, 0.6650, 0.0381]])

            c = numpy.array([1.0, 1.2, 3.0, 3.2])

            d = numpy.zeros((4,))
            for i in range(4):
                d[i] = sum(a[:,i]*(x - p[:,i])**2)

            return -(c.dot(numpy.exp(-d)))

        bounds = np.array([[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]], dtype=float)
        budget = 250
        x0 = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])

        optset = {'p': 0.5}
        res, histout, complete_history = \
             SQSnobFit.minimize(Hartman6, x0, bounds, budget, optset)

        # LIMIT:
        # fglob = -3.32236801141551
        # xglob = [0.20168952, 0.15001069, 0.47687398, 0.27533243, 0.31165162, 0.65730054]
        assert np.round(sum(res.optpar)-sum((0.2077, 0.14892, 0.4829, 0.2725, 0.31493, 0.66138)), 8) == 0