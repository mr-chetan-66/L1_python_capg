### main.py
### Entry point — handles user input, calls class-based DAO and utility functions

import db_config as db
import exam_dao as dao_module
import exam_util as util


def main():
    conn       = db.get_connection()
    exam_dao   = dao_module.ExamDao(conn)

    print("=" * 40)
    print("       EXAM RESULT MANAGEMENT SYSTEM")
    print("=" * 40)

    student_id = int(input("Enter Student ID : "))

    # Validate student ID
    if not util.is_valid_student_id(student_id):
        print("Invalid Student ID")
        return

    # Retrieve all results for the student
    results = exam_dao.retrieve_results_by_student(student_id)

    if not results:
        print("No Results Found")
        return

    # Display all results
    print("\nTotal Results Found :", util.get_result_count(results))
    print("-" * 40)

    for result in results:
        util.display_result(result)

    # Overall percentage and performance remark
    percentage = util.calculate_percentage(results)
    remark     = util.get_performance_remark(percentage)

    print("=" * 40)
    print("Overall Percentage :", percentage, "%")
    print("Performance Remark :", remark)

    # Pass / Fail summary
    summary = util.get_pass_fail_summary(results)
    print("Subjects Passed    :", summary['passed'])
    print("Subjects Failed    :", summary['failed'])
    print("=" * 40)

    # Best result using subquery in DAO
    best = exam_dao.retrieve_best_result(student_id)
    if best:
        print("\nBest Performing Subject:")
        print("  Subject        :", best.get_subject())
        print("  Marks Obtained :", best.get_marks_obtained(), "/", best.get_max_marks())
        print("  Grade          :", best.get_grade())
    print("=" * 40)

    # Delete a result record
    result_id = int(input("\nEnter Result ID to Delete (0 to skip) : "))

    if result_id != 0:
        if not util.is_valid_result_id(result_id):
            print("Invalid Result ID")
            return

        status = exam_dao.delete_result(result_id)
        print("Status :", status)

        # Show updated results after deletion
        if status == "Result Deleted Successfully":
            updated_results    = exam_dao.retrieve_results_by_student(student_id)
            updated_percentage = util.calculate_percentage(updated_results)

            print("\nUpdated Total Results   :", util.get_result_count(updated_results))
            print("Updated Percentage      :", updated_percentage, "%")


if __name__ == '__main__':
    main()
