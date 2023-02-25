from danni_framework.templator import render
from patterns.creational_patterns import Engine
from patterns.logger_singleton import Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, requests):
        return '200 OK', render('index.html', date=requests.get('date', None), objects_list=site.categories)


@AppRoute(routes=routes, url='/programs/')
class Programs:
    @Debug(name='Programs')
    def __call__(self, requests):
        return '200 OK', render('programs.html', date=requests.get('date', None))


@AppRoute(routes=routes, url='/contacts/')
class Contacts:
    @Debug(name='Contacts')
    def __call__(self, requests):
        return '200 OK', render('contacts.html', date=requests.get('date', None))


@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    def __call__(self, requests):
        logger.log('open course_list')
        try:
            category = site.find_category_by_id(int(requests['request_params']['id']))
            return '200 OK', render('courses-list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            logger.log('KeyError courses list')
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    def __call__(self, requests):
        if requests['method'] == 'POST':
            data = requests['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('web', name, category)

                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)

                site.courses.append(course)

            return '200 OK', render('courses-list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(requests['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                logger.log('KeyError create course')
                return '200 OK', 'No categories have been added yet'
            except ValueError:
                logger.log('ValueError category_id indefined')
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    def __call__(self, requests):
        if requests['method'] == 'POST':
            data = requests['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create-category.html',
                                    categories=categories)


@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    def __call__(self, requests):
        logger.log('open categories list')
        return '200 OK', render('category-list.html',
                                objects_list=site.categories)


@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    def __call__(self, requests):
        request_params = requests['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('courses-list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)

        except KeyError:
            logger.log('KeyError copy')
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student-list.html'


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create-student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add-student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
