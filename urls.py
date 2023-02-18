from views import Index, Programs, Contacts, CoursesList, CreateCourse, CreateCategory, CategoryList, CopyCourse
from datetime import date


def date_front(request: dict):
    request['date'] = date.today()


fronts = [date_front]

routes = {
    '/': Index(),
    '/programs/': Programs(),
    '/contacts/': Contacts(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-course/': CopyCourse()
}

