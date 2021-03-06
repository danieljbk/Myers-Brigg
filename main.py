import ast


def grouping_algorithm(student_data, members_per_group, duplicate_personality_limit):
    """
    student_data is a list of students whom we want to place into groups. Each student is a list containing their [personality, full name]
    members_per_group represents the size of the groups we will place students into
    duplicate_personality_limit represents the maximum number of duplicate personalities that we want in each group
    """

    # for each personality, which is the first term in each list, the three most compatible personalities are listem in the second term of each list.
    with open("assets/compatibilityList.txt", "r") as f:
        compatibility_chart = ast.literal_eval(f.read())

    """
    First, we want to figure out, from our data, which students are compatible with each other.
    There are many ways to record this data, and the method we chose is to find out all other students that each student is compatible with.
    """

    all_compatible_students_for_each_students = []

    for student in student_data:
        student_personality, student_name = student
        group = [student]
        student_favors = []

        for section in compatibility_chart:
            personality, personality_favors = section

            if student_personality == personality:
                student_favors = personality_favors

        for another_student in student_data:
            another_student_personality, another_student_name = another_student

            if another_student_personality in student_favors:
                group.append(another_student)

        all_compatible_students_for_each_students.append(group)

    """
    Now that we know who each student will be compatible with, we will evaluate each student and form a perfect group for them.
    We want each group to have a variety of possibilities, with no more than the duplicate_personality_limit.
    And, we don't want a student who has already been placed in a group to be placed again in another group.
    To handle that issue, when we finalize a group, we will also keep track of the students in the group.
    As we continue, we check whether each student we analyze has already been placed.
    If the group we are analyzing does not meet our standards (of a certain number of members and a duplicate limit), we will put the group off to the side.
    """

    successfully_matched_groups_of_students = []
    students_who_have_been_placed_in_a_group = []
    unsuccessful_groups = []

    for group in all_compatible_students_for_each_students:
        personalities_of_current_group_of_students = []
        current_group_of_students = []

        for student in group:
            if (
                student not in current_group_of_students
                and student not in students_who_have_been_placed_in_a_group
            ):
                student_personality = student[0]
                if (
                    personalities_of_current_group_of_students.count(
                        student_personality
                    )
                    < duplicate_personality_limit
                ):
                    current_group_of_students.append(student)
                    personalities_of_current_group_of_students.append(
                        student_personality
                    )
                if len(current_group_of_students) == members_per_group:
                    break

        if len(current_group_of_students) < members_per_group:
            unsuccessful_groups.append(group)
        else:
            for student in current_group_of_students:
                students_who_have_been_placed_in_a_group.append(student)
            successfully_matched_groups_of_students.append(current_group_of_students)

    """
    While our algorithm was able to group most of the students, it could not group all of them. 
    The remaining students, unluckily, were not placed in a perfect group. 
    To group these students, we will need to create less-diverse groups.
    We will now place compatible personalities in a single group without consideration for duplicates.
    """

    ungrouped_students = []
    for group in unsuccessful_groups:
        for student in group:
            if (
                student not in students_who_have_been_placed_in_a_group
                and student not in ungrouped_students
            ):
                ungrouped_students.append(student)

    return successfully_matched_groups_of_students, ungrouped_students


student_personalities_path = "assets/students.txt"
student_data = open(student_personalities_path, "r").readlines()
student_data = list(map(lambda student: student.strip().split(" ", 1), student_data))

members_per_group = 4

# we start with the limit of 2 personalities because choosing 1 as the limit actually leads to much less good groups forming
# this is the initial run of the function, for which we use the actual "student_data".
successfully_matched_groups_of_students, ungrouped_students = grouping_algorithm(
    student_data, members_per_group, 2
)

less_perfect_groups = []

for i in range(3, members_per_group + 1):
    if ungrouped_students:
        imperfectly_matched_groups_of_students, ungrouped_students = grouping_algorithm(
            ungrouped_students, members_per_group, i
        )
        less_perfect_groups.append(imperfectly_matched_groups_of_students)

with open("result.txt", "w") as result:

    for group_of_groups in less_perfect_groups:
        if group_of_groups:
            print("Found", len(group_of_groups), "groups:", file=result)
            for group in group_of_groups:
                print("   ", group, file=result)
            print("", file=result)

    print("Still ungrouped:", file=result)
    print("   ", len(ungrouped_students), ungrouped_students, file=result)

    """
    For our final step, we will output our results while distinguishing between the perfect groups and the flawed groups.
    """

    print("\n" * 1, "*" * 25, "\n" * 1, file=result)

    print(
        f"Formed {len(successfully_matched_groups_of_students)} Compatible Groups:",
        file=result,
    )

    group_count = 1
    grouped_students = []
    for group in successfully_matched_groups_of_students:
        print(f"\nGROUP {group_count}:", file=result)
        group_count += 1

        for student in group:
            line = (
                "    "
                + str(group.index(student) + 1)
                + ". "
                + student[1]
                + " "
                + f"({student[0]})"
            )
            print(line, file=result)

            if student in grouped_students:
                print("ERROR ??? DUPLICATE:", student, file=result)
            else:
                grouped_students.append(student)
