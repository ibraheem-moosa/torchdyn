"This file contains helper functions to construct Tableaus of explicit solvers RungeKutta4, DormandPrince45, Tsit45"
import torch
from collections import namedtuple

ExplicitRKTableau = namedtuple('ExplicitRKTableau', 'c, A, b_sol, b_err')


def construct_rk4(dtype):
    c = torch.tensor([0., 1 / 2, 1 / 2, 1], dtype=dtype)
    a = [
        torch.tensor([1 / 2], dtype=dtype),
        torch.tensor([0., 1 / 2], dtype=dtype),
        torch.tensor([0., 0., 1], dtype=dtype)]
    bsol = torch.tensor([1 / 6, 1 / 3, 1 / 3, 1 / 6], dtype=dtype)
    berr = torch.tensor([0.]) # for improved compatibility with utilities of other solvers, not technically true
    return (c, a, bsol, berr)


def construct_dopri5(dtype):
    c = torch.tensor([1 / 5, 3 / 10, 4 / 5, 8 / 9, 1., 1.], dtype=dtype)
    a = [
        torch.tensor([1 / 5], dtype=dtype),
        torch.tensor([3 / 40, 9 / 40], dtype=dtype),
        torch.tensor([44 / 45, -56 / 15, 32 / 9], dtype=dtype),
        torch.tensor([19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729], dtype=dtype),
        torch.tensor([9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656], dtype=dtype),
        torch.tensor([35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84], dtype=dtype),
    ]
    bsol = torch.tensor([35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0], dtype=dtype)
    berr = torch.tensor([1951 / 21600, 0, 22642 / 50085, 451 / 720, -12231 / 42400, 649 / 6300, 1 / 60.], dtype=dtype)
    return (c, a, bsol, bsol - berr)


def construct_tsit5(dtype):

    c = torch.tensor([
        161 / 1000,
        327 / 1000,
        9 / 10,
        .9800255409045096857298102862870245954942137979563024768854764293221195950761080302604,
        1.,
        1.
    ], dtype=dtype)
    a = [
        torch.tensor([
            161 / 1000
        ], dtype=dtype),
        torch.tensor([
            -.8480655492356988544426874250230774675121177393430391537369234245294192976164141156943e-2,
            .3354806554923569885444268742502307746751211773934303915373692342452941929761641411569
        ], dtype=dtype),
        torch.tensor([
            2.897153057105493432130432594192938764924887287701866490314866693455023795137503079289,
            -6.359448489975074843148159912383825625952700647415626703305928850207288721235210244366,
            4.362295432869581411017727318190886861027813359713760212991062156752264926097707165077
        ], dtype=dtype),
        torch.tensor([
            5.325864828439256604428877920840511317836476253097040101202360397727981648835607691791,
            -11.74888356406282787774717033978577296188744178259862899288666928009020615663593781589,
            7.495539342889836208304604784564358155658679161518186721010132816213648793440552049753,
            -.9249506636175524925650207933207191611349983406029535244034750452930469056411389539635e-1
        ], dtype=dtype),
        torch.tensor([
            5.861455442946420028659251486982647890394337666164814434818157239052507339770711679748,
            -12.92096931784710929170611868178335939541780751955743459166312250439928519268343184452,
            8.159367898576158643180400794539253485181918321135053305748355423955009222648673734986,
            -.7158497328140099722453054252582973869127213147363544882721139659546372402303777878835e-1,
            -.2826905039406838290900305721271224146717633626879770007617876201276764571291579142206e-1
        ], dtype=dtype),
        torch.tensor([
            .9646076681806522951816731316512876333711995238157997181903319145764851595234062815396e-1,
            1 / 100,
            .4798896504144995747752495322905965199130404621990332488332634944254542060153074523509,
            1.379008574103741893192274821856872770756462643091360525934940067397245698027561293331,
            -3.290069515436080679901047585711363850115683290894936158531296799594813811049925401677,
            2.324710524099773982415355918398765796109060233222962411944060046314465391054716027841
        ], dtype=dtype),
    ]
    bsol = torch.tensor([
        .9646076681806522951816731316512876333711995238157997181903319145764851595234062815396e-1,
        1 / 100,
        .4798896504144995747752495322905965199130404621990332488332634944254542060153074523509,
        1.379008574103741893192274821856872770756462643091360525934940067397245698027561293331,
        -3.290069515436080679901047585711363850115683290894936158531296799594813811049925401677,
        2.324710524099773982415355918398765796109060233222962411944060046314465391054716027841,
        0.
    ], dtype=dtype)
    berr = torch.tensor([
        .9468075576583945807478876255758922856117527357724631226139574065785592789071067303271e-1,
        .9183565540343253096776363936645313759813746240984095238905939532922955247253608687270e-2,
        .4877705284247615707855642599631228241516691959761363774365216240304071651579571959813,
        1.234297566930478985655109673884237654035539930748192848315425833500484878378061439761,
        -2.707712349983525454881109975059321670689605166938197378763992255714444407154902012702,
        1.866628418170587035753719399566211498666255505244122593996591602841258328965767580089,
        1 / 66.,
    ], dtype=dtype)
    return (c, a, bsol, bsol - berr)


########################
# Interpolator coeff 
########################

def construct_4th(dtype):
    "4th order interpolator for `dopri5`"
    bmid = torch.tensor([
        0.10013431883002395, 0, 0.3918321794184259, -0.02982460176594817,
        0.05893268337240795, -0.04497888809104361, 0.023904308236133973
        ], dtype=dtype)
    return bmid
    