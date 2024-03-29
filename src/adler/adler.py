import argparse
import astropy.units as u

from adler.dataclasses.AdlerPlanetoid import AdlerPlanetoid
from adler.science.PhaseCurve import PhaseCurve


def runAdler(args):
    planetoid = AdlerPlanetoid.construct_from_RSP(args.ssoid, args.filter_list, args.date_range)

    # now let's do some phase curves!

    # get the RSP r filter model
    pc = PhaseCurve(
        abs_mag=planetoid.SSObject.H[2] * u.mag,
        phase_param=planetoid.SSObject.G12[2],
        model_name="HG12_Pen16",
    )
    print(pc)
    print(pc.abs_mag, pc.phase_param)

    # get the r filter observations
    obs_r = planetoid.observations_in_filter("r")
    alpha = obs_r.phaseAngle * u.deg
    red_mag = obs_r.reduced_mag * u.mag
    mag_err = obs_r.magErr * u.mag

    # do a simple fit to all data
    pc_fit = pc.FitModel(alpha, red_mag, mag_err)
    print(pc_fit)


def main():
    parser = argparse.ArgumentParser(description="Runs Adler for a select planetoid and given user input.")

    parser.add_argument("-s", "--ssoid", help="SSObject ID of planetoid.", type=str, required=True)
    parser.add_argument(
        "-f", "--filters", help="Comma-separated list of filters required.", type=str, default="u,g,r,i,z,y"
    )
    parser.add_argument(
        "-d",
        "--date_range",
        help="Minimum and maximum MJD(TAI) of required observations. Default is to pull all observations.",
        nargs=2,
        type=float,
        default=[60000.0, 67300.0],
    )

    args = parser.parse_args()

    args.filter_list = args.filters.split(",")

    runAdler(args)


if __name__ == "__main__":
    main()
