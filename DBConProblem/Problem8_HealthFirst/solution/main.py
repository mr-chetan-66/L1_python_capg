# Please do not change the skeleton code given here.
import utility as ut
import health_service as hs
import health_exception as he


def display(obj):
    print(f"\nClaim Id: {obj.get_claim_id()}")
    print(f"Patient Name: {obj.get_patient_name()}")
    print(f"Policy Id: {obj.get_policy_id()}")
    print(f"Policy Type: {obj.get_policy_type()}")
    print(f"Claim Date: {obj.get_claim_date()} 00:00:00")
    print(f"Claim Amount: {obj.get_claim_amount()}")
    print(f"Coverage Amount: {obj.get_coverage_amount()}")
    print(f"Deductible: {obj.get_deductible()}")
    print(f"Approved Amount: {obj.get_approved_amount()}")


def main():
    records = ut.read_file("InsuranceClaims.txt")
    obj = hs.HealthService()
    obj.read_data(records)

    top = obj.find_top3_policies()
    print("Top 3 Policies:")
    for k, v in top.items():
        print(f"{k} : {v}")

    claim_id = input("\nEnter the claim id to search: ")
    try:
        ut.validate_claim_id(claim_id)
        result = obj.search_claim(claim_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except he.InvalidClaimIdException as e:
        print(e.get_message())

    s = ut.convert_date(input("\nEnter the start claim date (DD/MM/YYYY): "))
    e = ut.convert_date(input("Enter the end claim date (DD/MM/YYYY): "))
    hv = obj.find_high_value_claims(s, e)

    if not hv:
        print("No high value claims found in the specified date range")
        return

    print("Claims with amount > 100000:")
    for k, v in hv.items():
        print(f"{k} : {v}")

    policy_type = input("\nEnter the policy type for approved amount update: ")
    updated = obj.update_approved_amount(policy_type)
    if updated is None:
        print("No records updated")
    else:
        print("\nThe updated claim details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
