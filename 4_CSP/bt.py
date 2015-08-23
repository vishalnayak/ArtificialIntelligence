__author__ = 'vishal'
import collections
import sys


class CSP(object):
    """
    Class containing the complete problem statement.
    Also contains the following:
    List of all course names.
    List of lists containing timings for all the courses.
    List of lists containing recitation timings.
    List of lists containing domains of each course.
    List of number of students required for courses.
    List of lists containing the TA skills required by courses.
    List containing ta presence requirement in courses.
    List of TA objects.
    List of lists containing TAs assigned for courses.
    List of lists containing courses assigned to TAs.

    Order in which items are added to these lists determines which course/TA the entry belongs to.
    """

    def __init__(self):
        self.course_list = []
        self.course_timings_list = []
        self.course_recitation_timings_list = []
        self.course_domains_list = []
        self.num_of_students_list = []
        self.req_num_of_ta_list = []
        self.req_ta_skills_list = []
        self.ta_attends_list = []
        self.ta_object_list = []
        self.ta_to_course_assignments = []
        self.course_to_ta_assignments = []

    def __str__(self):
        i = 0
        ret_str = ''
        for x in self.course_list:
            ret_str += str(i + 1) + ' ' + x + str(self.ta_to_course_assignments[i]) + '\n'
            i += 1
        return ret_str


class TA(object):
    """
    Object holding information about TAs.
    The name, skill sets and availability information.
    """

    def __init__(self):
        self.name = None
        self.skills = []
        self.classes = []
        self.availability = 1
        self.index = 0

    def __str__(self):
        return self.name


def print_course_to_ta_assignments(cp):
    """
    Prints the assignments ordered by TAs.
    """
    ta_index = 0
    print '\n== Courses assignted to TAs =='
    for entry in cp.course_to_ta_assignments:
        if len(entry) is not 0:
            print cp.ta_object_list[ta_index].name + ": ",
            print entry
        ta_index += 1


def print_ta_to_course_assignments(cp):
    """
    Prints the assignments ordered by Courses.
    """
    course_index = 0
    print '\n== TAs assigned to Courses =='
    for entry in cp.ta_to_course_assignments:
        if len(entry) is not 0:
            print cp.course_list[course_index] + ": ",
            print entry,
            print 'and Need: ' + str(cp.req_num_of_ta_list[course_index])
        course_index += 1


def filter_skill_set_mismatch(csp):
    """
    From the domains of each course, filter out those TAs whose skill sets do not match with the course requirements.
    """
    course = 0
    for course_req_list in csp.req_ta_skills_list:
        domains = csp.course_domains_list[course]
        for ta in domains[:]:
            if set(ta.skills).issubset(course_req_list) is not True:
                domains.remove(ta)
            elif len(ta.skills) is 0:
                domains.remove(ta)
        course += 1


def filter_recitation_overlap(csp):
    """
    From the domains of each course, filter out those TAs whose class timings overlap with the course recitation timings.
    """
    course = 0
    for domains in csp.course_domains_list:
        for ta in domains[:]:
            ta_multiset = collections.Counter(ta.classes)
            recit_multiset = collections.Counter(csp.course_recitation_timings_list[course])
            """
            Remove the overlaps
            """
            if len(list((ta_multiset & recit_multiset).elements())) > 0:
                domains.remove(ta)
        course += 1


def filter_class_timings_overlap(csp):
    """
    From the domains of each course, filter out those TAs whose class timings overlap with the course lecture timings and TAs are required to attend the lectures.
    """
    course = 0
    for attend in csp.ta_attends_list:
        """
        Checking if TA is required to attend the lectures
        """
        if attend is 'yes':
            domains = csp.course_domains_list[course]
            for ta in domains[:]:
                ta_classes_list = ta.classes
                course_timings_list = csp.course_timings_list[course]
                ta_multiset = collections.Counter(ta_classes_list)
                course_timings_multiset = collections.Counter(course_timings_list)
                overlaps = list((ta_multiset & course_timings_multiset).elements())
                """
                Remove the overlaps
                """
                if len(overlaps) > 0:
                    domains.remove(ta)
    course += 1


def is_complete(assignments):
    """
    Check if the assignments are completed
    """
    found = False
    for x in assignments:
        if len(x) is not 0:
            found = True
        if found is True and len(x) is 0:
            return 'partial', False
    if found is True:
        return 'complete', True
    return 'failure', False


def select_unassigned_variable(csp):
    """
    Picks the next course for assigning TAs
    """
    i = 0
    for x in csp.ta_to_course_assignments:
        if len(x) is 0:
            return i
        i += 1


def num_of_ta(students):
    """
    Calculates the number of TAs required by the course, depending on number of students enrolled.
    """
    if 25 <= students < 40:
        return 0.5
    if 40 <= students < 60:
        return 1.5
    if students >= 60:
        return 2
    return 0


def parse_course_schedules(csp, entries):
    """
    Parses and stores in the CSP class object, the input containing course schedules
    """
    course_index = -1
    if entries[0] in csp.course_list:
        course_index = csp.course_list.index(entries[0])
        csp.course_timings_list[course_index] = [entries[2 * x + 1] + "_" + entries[2 * x + 2] for x in
                                                 range((len(entries) - 1) / 2)]
    else:
        csp.course_list.append(entries[0])
        csp.course_timings_list = [entries[2 * x + 1] + "_" + entries[2 * x + 2] for x in range((len(entries) - 1) / 2)]
        # Defaults for courses
        csp.course_recitation_timings_list.append([])
        csp.num_of_students_list.append(0)
        csp.ta_attends_list.append('NO')
        csp.ta_to_course_assignments.append([])
        csp.req_ta_skills_list.append([])


def parse_course_recitation(csp, entries):
    """
    Parses and stores in the CSP class object, the input containing course recitation information
    """
    if entries[0] in csp.course_list:
        course_index = csp.course_list.index(entries[0])
        y = [entries[2 * x + 1] + "_" + entries[2 * x + 2] for x in range((len(entries) - 1) / 2)]
        csp.course_recitation_timings_list[course_index] = y


def parse_course_details(csp, entries):
    """
    Parses and stores in the CSP class object, the input containing course details
    """
    if entries[0] in csp.course_list:
        course_index = csp.course_list.index(entries[0])
        csp.num_of_students_list[course_index] = int(entries[1])
        csp.ta_attends_list[course_index] = entries[2]


def parse_course_requirements(csp, entries):
    """
    Parses and stores in the CSP class object, the input containing course requirements
    """
    if entries[0] in csp.course_list:
        course_index = csp.course_list.index(entries[0])
        csp.req_ta_skills_list[course_index] = entries[1:]


def parse_ta_responsibilities(csp, entries):
    """
    Parses and stores in the CSP class object, the input containing TA responsibilities
    """
    ta = TA()
    ta.name = entries[0]
    ta.classes = [entries[2 * x + 1] + "_" + entries[2 * x + 2] for x in range((len(entries) - 1) / 2)]
    ta.index = len(csp.ta_object_list)
    csp.ta_object_list.append(ta)
    # Defaults for TA
    csp.course_to_ta_assignments.append([])


def parse_ta_skills(csp, entries):
    """
    Parses and stores in the CSP class object, the input containing TA skills
    """
    ta_index = -1
    for x in csp.ta_object_list:
        ta_index += 1
        if entries[0] == x.name:
            break
    if entries[0] is not -1:
        for x in entries[1:]:
            csp.ta_object_list[ta_index].skills.append(x)


def forward_check(course, ta, csp):
    """
    After assigning TA 'ta' for course 'course', check if all the unassigned courses have valid domains.
    """
    print 'Forward checking for course: ' + str(csp.course_list[course]) + ' after assigning TA: ' + str(ta.name)
    course_index = course

    if course_index == len(csp.course_list) - 1:
        return 'success'

    """
    Iterate through all the unassigned courses and check if the domains are empty
    """
    while course_index < len(csp.course_list):
        domains = csp.course_domains_list[course_index]
        for domain in domains:
            if course_index != course and domain.availability == 0.0 and ta.name == domain.name:
                print 'Forward-checking fault. ' \
                      '\nCourse being processed:' + str(csp.course_list[course]) + \
                      '\nForward checked course:' + str(csp.course_list[course_index]) + ", TA:" + str(domain.name)
                return 'failure'
        course_index += 1

    return 'success'


def consistency_check(course, csp):
    """
    Apply arc consistency on the courses.
    """
    print 'Checking consistency for course: ' + str(csp.course_list[course])
    queue = [x for x in range(len(csp.course_list))]
    while len(queue) > 0:
        element = queue[0]
        queue = queue[1:]
        neighbors = neighbors_of_course(csp, element)
        for neighbor in neighbors:
            if remove_inconsistency(csp, element, neighbor):
                if neighbor not in queue:
                    queue.append(neighbor)

    course_index = course

    """
    After the consistency check, iterate through all the unassigned domains and check if the domains are empty.
    """
    if course_index == len(csp.course_list) - 1:
        return 'success'
    course_index += 1
    avail = 0
    while course_index < len(csp.course_list):
        domains = csp.course_domains_list[course_index]
        for domain in domains:
            avail += domain.availability
        if avail == 0:
            print 'Consistency fault. ' \
                  '\nCourse with TA scarcity:' + str(csp.course_list[course_index])
            return 'failure'
        else:
            avail = 0
        course_index += 1

    return 'success'


def neighbors_of_course(csp, course):
    """
    Sub-routine of arc-consistency to find out the neighbors of a domain so that consistency can be applied.
    """
    neighbors = []
    for domain in csp.course_domains_list[course]:
        for other_course in range(len(csp.course_list)):
            if course != other_course:
                for other_domain in csp.course_domains_list[other_course]:
                    if domain.name == other_domain.name:
                        if other_course not in neighbors:
                            neighbors.append(other_course)
    return neighbors


def remove_inconsistency(csp, a, b):
    """
    Check if the neighbouring nodes' domains are affected by current assignment. If yes, remove the domain from current node and continue.
    """
    req_a = csp.req_num_of_ta_list[a]
    req_b = csp.req_num_of_ta_list[b]

    domains_a = csp.course_domains_list[a]
    domains_b = csp.course_domains_list[b]
    removed = False
    for domain_a in domains_a[:]:
        """
        Consider only the remaining availability of TA that is being assigned.
        """
        usage_a = 0
        if req_a >= domain_a.availability:
            usage_a = domain_a.availability
        else:
            usage_a = req_a
        arc_consistent = False
        capacity = 0
        for domain_b in domains_b:
            if domain_a.name == domain_b.name:
                capacity += domain_b.availability - usage_a
            else:
                capacity += domain_b.availability
            if capacity >= req_b:
                arc_consistent = True
                break
        """
        Remove the inconsistent domain here
        """
        if arc_consistent is False:
            domains_a.remove(domain_a)
            removed = True
    return removed


def recursive_solver(csp, with_forward_checking, with_constraint_propagation):
    """
    Same recursive solver for bt, bt+fc and bt+fc+cp strategies.
    Variations are controlled by parameters of this method.
    """
    ta_to_course = csp.ta_to_course_assignments
    course_to_ta = csp.course_to_ta_assignments

    result, status = is_complete(ta_to_course)
    if status is True:
        return 'solution'

    course = select_unassigned_variable(csp)

    for ta in csp.course_domains_list[course]:
        if ta.availability > 0:
            delta = 0
            if csp.req_num_of_ta_list[course] >= ta.availability:
                csp.req_num_of_ta_list[course] -= ta.availability
                delta = ta.availability
                ta.availability = 0.0
            else:
                ta.availability -= csp.req_num_of_ta_list[course]
                delta = csp.req_num_of_ta_list[course]
                csp.req_num_of_ta_list[course] = 0.0

            """
            Forward checking after an assignment.
            """
            if with_forward_checking and 'failure' == forward_check(course, ta, csp):
                return 'failure'

            """
            Constraint propagation after an assignment
            """
            if with_constraint_propagation and 'failure' == consistency_check(course, csp):
                print_domains(csp)
                return 'failure'

            """
            Adding the entry as an assignment, if there were no issues with checks.
            """
            ta_to_course[course].append((ta.name, delta))
            course_to_ta[ta.index].append((csp.course_list[course], delta))

            """
            Continuing with the recursive solution of assigning TAs to other courses.
            """
            status = recursive_solver(csp, with_forward_checking, with_constraint_propagation)
            if status != 'failure':
                return 'solution'

            """
            If the assignment fails, remove the entry from the solution lists.
            """
            ta_to_course[course].remove((ta.name, delta))
            course_to_ta[ta.index].remove((csp.course_list[course], delta))
            ta.availability += delta
    return 'failure'


def solve(csp, with_forward_checking, with_constraint_propagation):
    """
    Invoking the search strategies for bt, bt+fc, bt+fc+c strategies.
    """
    if with_constraint_propagation and 'failure' == consistency_check(0, csp):
        """
        Consistency check before invoking the recursing solver failed.
        """
        print_domains(csp)
        return 'failure'
    return recursive_solver(csp, with_forward_checking, with_constraint_propagation)


def print_domains(csp):
    """
    Prints out all the domains present in the courses.
    """
    print '\n==Course Domains after filtering=='
    course_index = 0
    for x in csp.course_domains_list:
        print csp.course_list[course_index],
        print ': ',
        for y in x:
            print str(y) + "(" + str(y.availability) + ')',
        print '\n'
        course_index += 1


def main():
    """
    Create a CSP object to hold the problem statement and to hold the intermediate solutions.
    """
    csp = CSP()

    """
    Read the input file from the argument
    """
    f = open(sys.argv[1], 'r')
    i = 0
    line_num = 0
    for line in f:
        line_num += 1
        if len(line) is 1:
            i += 1
            if i is 6:
                break
            continue

        entry_list = line.split(',')
        entry_list = map(lambda x: x.strip().upper().replace(' ', '_'), entry_list)

        if i is 0:
            # Course Schedules
            parse_course_schedules(csp, entry_list)
        elif i is 1:
            # Course recitations
            parse_course_recitation(csp, entry_list)
        elif i is 2:
            # Course details
            parse_course_details(csp, entry_list)
        elif i is 3:
            # Course requirements
            parse_course_requirements(csp, entry_list)
        elif i is 4:
            # TA responsibilities
            parse_ta_responsibilities(csp, entry_list)
        elif i is 5:
            # TA Skills
            parse_ta_skills(csp, entry_list)

    """
    Append to all TAs to all domains, initially
    """
    y = [x for x in csp.ta_object_list]
    for x in csp.course_list:
        csp.course_domains_list.append(y[:])

    """
    Calculate the number of TAs required and fill in the CSP
    """
    csp.req_num_of_ta_list = map(num_of_ta, csp.num_of_students_list)


    """
    Filter out recitation overlaps
    """
    filter_recitation_overlap(csp)

    """
    Filter out lecture timings overlaps
    """
    filter_class_timings_overlap(csp)

    """
    Filter out skill set mismatches
    """
    filter_skill_set_mismatch(csp)

    """
    Domains before the search procedure is invoked
    """
    print_domains(csp)

    print 'Required TA: ' + str(csp.req_num_of_ta_list)
    print '\n'

    """
    Uncomment ONLY ONE of the three strategies below.
    """
    import timeit
    start_time = timeit.default_timer()

    """
    Backtracking only
    """
    status = solve(csp, False, False)

    """
    Backtracking + Forward Checking
    """
    # status = solve(csp, True, False)

    """
    Backtracking + Forward Checking + Constraint Propagation
    """
    # status = solve(csp, True, True)

    time_taken = timeit.default_timer() - start_time
    print 'TimeTaken: ' + str(time_taken)
    if status is 'solution':
        print 'Backtracking Successful!'
        print_course_to_ta_assignments(csp)
        print_ta_to_course_assignments(csp)
    else:
        print 'Backtracking Failed. Resource unavailable.'


if __name__ == '__main__':
    main()