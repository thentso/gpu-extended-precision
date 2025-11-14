from fpanAlgs import twoSum, split, twoProd, ddadd, madd, ddmul, mmul, DDFloat, MFloat
from fractions import Fraction
from decimal import Decimal, getcontext
import math

# Test the 5 different datatypes for multiplication (evaluating on a common expression a*b + c*d*e)

def evalFloat(a, b, c, d, e):
    return a*b + c*d*e

def evalFrac(a, b, c, d, e):
    A, B, C, D, E = map(Fraction, (a, b, c, d, e))
    return A*B + C*D*E

getcontext().prec = 50
def evalDecimal(a, b, c, d, e):
    A, B, C, D, E = map(Decimal, (a, b, c, d, e))
    return A*B + C*D*E

def evalDD(a, b, c, d, e):
    return DDFloat(a, 0) * DDFloat(b, 0) + DDFloat(c, 0) * DDFloat(d, 0) * DDFloat(e, 0)

def evalM(a, b, c, d, e):
    return MFloat(a, 0) * MFloat(b, 0) + MFloat(c, 0) * MFloat(d, 0) * MFloat(e, 0)




TEST_CASES = [
    (8.834235326183948e71,  9.578097123275567e53,
     -4.6316785776358486e77, -2.55523157298961e61,
     -4.6316697434005227e77, -2.037703193040189e60,
     -4.6316697434005227e77, -2.0377031930401882e60),

    (1.4919697328456323e87, 5.521397077432451e70,
     4.973223565419703e86, -4.909094196809657e-91,
     1.9892920893876027e87, -4.909094196809657e-91,
     1.9892920893876027e87,  0.0),

    (-8191.992462158203,     9.143899130258214e-100,
     -9.14613152750686e-100, 2.242825269339505e-117,
     -8191.992462158203,    -2.2323972486468995e-103,
     -8191.992462158203,    -2.232397248646922e-103),

    (-6.344854596578372e-117, 3.5220749571797036e-133,
     4.417117661946964e71,   6.502419267294956e-117,
     4.417117661946964e71,    1.5756467071658512e-118,
     4.417117661946964e71,    1.5756467071658477e-118),

    (-1.6110451730902522e60,  1.3071815033235768e39,
     -2.1567956686498734e68,  1.1972619985767064e52,
     -2.156795684760325e68,  -4.863878519471706e51,
     -2.156795684760325e68,  -4.8638785194717065e51),

    (8.84443087277937e-75,   -2.4072299075463057e-91,
     1.7413332937543717e45, -8.843436600161344e-75,
     1.7413332937543717e45,   9.942726180261331e-79,
     1.7413332937543717e45,   9.942726180263738e-79),
]

def testExpression():
    getcontext().prec = 50

    a, b, c, d, e = 1.23, 4.56, 7.89, 0.12, 3.45

    truth = evalDecimal(a, b, c, d, e)

    for name, fn in [
        ("Float",    evalFloat),
        ("Fraction", evalFrac),
        ("DDFloat",  evalDD),
        ("MFloat",   evalM),
    ]:
        out = fn(a, b, c, d, e)

        if hasattr(out, "x0") and hasattr(out, "x1"):
            # not using high precision can cause the error precision to actually not get added! (i.e 1e16 + 1 goes unnoticed)
            Dx0 = Decimal(out.x0)
            Dx1 = Decimal(out.x1)
            val = Dx0 + Dx1    
        elif isinstance(out, Fraction):
            val = Decimal(out.numerator) / Decimal(out.denominator)
        else:
            val = Decimal(out)
        # Converting it into a decimal allows for highest precision
        err = abs(val - truth)

        print(f"{name:<8} -> {val:.10E}, error = {err:.2E}")
        # : gives format specifiers (< is left alight w/ number being field width, .num is precision, E is in scientific/exponential notation)


def test_division(a: float, b: float):
    getcontext().prec = 50
    truth = Decimal(a) / Decimal(b)

    float_val = a / b
    dd = DDFloat(a, 0) / DDFloat(b, 0)
    m = MFloat(a, 0) / MFloat(b, 0)

    # 3) helper to collapse a result into a Decimal
    def to_decimal(x):
        # if it’s a double-term expansion
        if hasattr(x, "x0") and hasattr(x, "x1"):
            return Decimal(x.x0) + Decimal(x.x1)
        # if you ever want to handle Fraction, add an isinstance check here
        return Decimal(x)

    # 4) build a table of (name, value, error)
    rows = [
        ("Float",    to_decimal(float_val)),
        ("DDFloat",  to_decimal(dd)),
        ("MFloat",   to_decimal(m)),
    ]

    # 5) print nicely
    print(f"{'Method':<8}  {'Value':<17}   {'Error':<12}")
    for name, dec_val in rows:
        err = abs(dec_val - truth)
        # .12E shows 12 digits after decimal in scientific form
        print(f"{name:<8}  {dec_val:.12E}   {err:.2E}")

def test_sqrt(a: float):
    getcontext().prec = 50
    truth = Decimal(a).sqrt()

    float_val = math.sqrt(a)
    dd = DDFloat(a,0).sqrt()
    m = MFloat(a, 0).sqrt()
    
     # 3) helper to collapse a result into a Decimal
    def to_decimal(x):
        # if it’s a double-term expansion
        if hasattr(x, "x0") and hasattr(x, "x1"):
            return Decimal(x.x0) + Decimal(x.x1)
        # if you ever want to handle Fraction, add an isinstance check here
        return Decimal(x)

    # 4) build a table of (name, value, error)
    rows = [
        ("Float",    to_decimal(float_val)),
        ("DDFloat",  to_decimal(dd)),
        ("MFloat",   to_decimal(m)),
    ]

    # 5) print nicely
    print(f"{'Method':<8}  {'Value':<17}   {'Error':<12}")
    for name, dec_val in rows:
        err = abs(dec_val - truth)
        # .12E shows 12 digits after decimal in scientific form
        print(f"{name:<8}  {dec_val:.12E}   {err:.2E}")







    
if __name__ == "__main__":
    for i, (x0, x1, y0, y1, dd0_exp, dd1_exp, m0_exp, m1_exp) in enumerate(TEST_CASES, 1):   # syntax starts i at 1, but still is using each case and forgetting the 0th
        dd0_act, dd1_act = ddadd(x0, x1, y0, y1)
        m0_act,  m1_act  = madd(x0, x1, y0, y1)

        print(f"\n=== Case #{i} ===")
        print(" Inputs: x0=", x0, " x1=", x1, " y0=", y0, " y1=", y1)
        print(" ddadd → actual:   ", (dd0_act, dd1_act))
        print("        expected: ", (dd0_exp, dd1_exp))
        print(" match? ", (dd0_act, dd1_act) == (dd0_exp, dd1_exp))

        print(" madd  → actual:   ", (m0_act, m1_act))
        print("        expected: ", (m0_exp, m1_exp))
        print(" match? ", (m0_act, m1_act) == (m0_exp, m1_exp))


    testExpression()
    test_division(1.24, 3.56)
    test_sqrt(5.3)