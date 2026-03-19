# Please do not change the skeleton code given here.
import utility as ut
import lib_service as ls
import lib_exception as le


def display(obj):
    print(f"\nIssue Id: {obj.get_issue_id()}")
    print(f"Member Name: {obj.get_member_name()}")
    print(f"Book Code: {obj.get_book_code()}")
    print(f"Genre: {obj.get_genre()}")
    print(f"Member Type: {obj.get_member_type()}")
    print(f"Issue Date: {obj.get_issue_date()} 00:00:00")
    print(f"Due Date: {obj.get_due_date()} 00:00:00")
    print(f"Return Date: {obj.get_return_date()} 00:00:00")
    print(f"Overdue Days: {obj.get_overdue_days()}")
    print(f"Fine Per Day: {obj.get_fine_per_day()}")
    print(f"Total Fine: {obj.get_total_fine()}")


def main():
    records = ut.read_file("BookIssues.txt")
    obj = ls.LibraService()
    obj.read_data(records)

    top = obj.find_top3_books()
    print("Top 3 Books:")
    for k, v in top.items():
        print(f"{k} : {v}")

    issue_id = input("\nEnter the issue id to search: ")
    try:
        ut.validate_issue_id(issue_id)
        result = obj.search_issue(issue_id)
        if result is None:
            print("No record found")
        else:
            display(result)
    except le.InvalidIssueIdException as e:
        print(e.get_message())

    s = ut.convert_date(input("\nEnter the start return date (DD/MM/YYYY): "))
    e = ut.convert_date(input("Enter the end return date (DD/MM/YYYY): "))
    od = obj.find_overdue_issues(s, e)

    if not od:
        print("No overdue issues found in the specified date range")
        return

    print("Issues with overdue days > 5:")
    for k, v in od.items():
        print(f"{k} : {v}")

    member_type = input("\nEnter the member type for fine update: ")
    updated = obj.update_fine(member_type)
    if updated is None:
        print("No records updated")
    else:
        print("\nThe updated issue details are:")
        for o in updated:
            display(o)


if __name__ == "__main__":
    main()
