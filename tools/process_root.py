#!/usr/bin/env python


def process_root(input_charge, input_light):
    params.file_label = "_".join(input_light.split("_")[-2:]).split(".")[0]

    output_charge = f"{params.file_label}/charge_df_{params.file_label}.bz2"

    inpur_light = f"{params.file_label}/light_df_{params.file_label}.bz2"

    match_file = f"{params.file_label}/match_dict_{params.file_label}.json"

    charge_df = load_charge(input_charge)
    light_df = load_light(input_light)
    match_dict = match_events(charge_df, light_df)

    # Remove light events without charge event match
    light_events = np.unique(ak.flatten(match_dict.values()))
    light_df = light_df[light_df["event"].isin(light_events)]

    # Remove charge events without associated light event
    charge_df = charge_df.loc[int(match_dict.keys())]

    # Flip x axis
    charge_df["event_hits_x"] = charge_df["event_hits_x"].apply(
        lambda x: [np.power(-1, params.flip_x) * i for i in x]
    )
    light_df["x"] = light_df["x"].apply(lambda x: np.power(-1, params.flip_x) * x)

    # Save files
    os.makedirs(params.file_label, exist_ok=True)
    charge_df.to_csv(output_charge)
    light_df.to_csv(inpur_light)
    with open(match_file, "w") as f:
        json.dump(match_dict, f)

    print("Processing completed.")

    return charge_df, light_df, match_dict


if __name__ == "__main__":
    from argparse import ArgumentParser

    from methods import (
        ak,
        json,
        load_charge,
        load_light,
        match_events,
        np,
        os,
        params,
    )

    parser = ArgumentParser()
    parser.add_argument("light", help="Path to light file")
    parser.add_argument("charge", help="Path to charge file")

    args = parser.parse_args()

    input_charge = args.charge
    input_light = args.light

    _, _, _ = process_root(input_charge, input_light)

else:
    from .methods import (
        ak,
        json,
        load_charge,
        load_light,
        match_events,
        np,
        os,
        params,
    )
