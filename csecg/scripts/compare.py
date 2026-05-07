import random

import numpy

import csecg
import csecg.loader.ptbdb
import csecg.util

DURATION = 1000  # 1 second
CR = 10


def main() -> None:
    if not csecg.util.dataset_exists():
        print("Missing dataset... Download via `python -m csecg.util.download_dataset`")
        return

    controls = [
        csecg.util.DATASET / "patient121" / "s0311lre",
        csecg.util.DATASET / "patient156" / "s0299lre",
        csecg.util.DATASET / "patient182" / "s0308lre",
        csecg.util.DATASET / "patient236" / "s0462_re",
        csecg.util.DATASET / "patient263" / "s0499_re",
    ]
    leads = ['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']
    prd_per_lead = {key: {'lasso': [], 'group_lasso': []} for key in leads}

    psi = csecg.basis_matrix(DURATION)

    for control in controls:
        # Look at a random 1 second chunk for each patient
        chunk = random.randint(0, 30000)
        channel_names, signals = csecg.loader.ptbdb.load_12_lead_record(
            control,
            sampfrom=chunk,
            sampto=chunk + DURATION,
        )
        ecg = csecg.Ecg(channel_names, signals)

        # Compress the signal
        phi = csecg.sensing_matrix(ecg, CR)
        compressed_data = phi @ ecg.signals

        # Recover with LASSO / Group LASSO
        lasso_coefs = csecg.lasso_solver(compressed_data, phi, psi)
        group_lasso_coefs = csecg.group_lasso_solver(compressed_data, phi, psi)

        # Recover the signal
        lasso_signals = psi @ lasso_coefs
        group_lasso_signals = psi @ group_lasso_coefs

        # Calculate PRD per channel
        print(f"\n\nPatient {control.as_posix()}\nLead\t | Lasso\t | Group Lasso")
        for lead, source, lasso_recovered, group_lasso_recovered in zip(
            ecg.channel_names,
            ecg.signals.T,
            lasso_signals.T,
            group_lasso_signals.T,
        ):
            lasso_prd = csecg.prd(source, lasso_recovered)
            group_lasso_prd = csecg.prd(source, group_lasso_recovered)
            prd_per_lead[lead]['lasso'].append(lasso_prd)
            prd_per_lead[lead]['group_lasso'].append(group_lasso_prd)
            print(f"{lead} \t | {lasso_prd:.2f}%\t | {group_lasso_prd:.2f}%")

    # Average PRD
    print(f"\n\nAverage PRD, CR = {CR}\nLead\t | Lasso\t | Group Lasso")
    for lead, prd in prd_per_lead.items():
        print(f"{lead} \t | {numpy.mean(prd['lasso']):.2f}%\t | {numpy.mean(prd['group_lasso']):.2f}%")


if __name__ == "__main__":
    main()
