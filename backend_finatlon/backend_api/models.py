import os
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, RegexValidator

# =============================================================================
# Вспомогательные функции валидации
# =============================================================================

def validate_okso_code(value):
    """Проверяет соответствие кода ОКСО маске 00.00.00"""
    if not re.match(r'^\d{2}\.\d{2}\.\d{2}$', value):
        raise ValidationError('Код специальности должен быть в формате 00.00.00')


def validate_file_extension(value, allowed_extensions):
    """Универсальная проверка расширения файла"""
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f'Допустимые расширения: {", ".join(allowed_extensions)}')


# Специализированные валидаторы для каждого поля
def validate_work_file(value):
    """Проверяет расширение файла работы: .doc, .docx"""
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext not in ['doc', 'docx']:
        raise ValidationError('Допустимые расширения: doc, docx.')


def validate_title_page_file(value):
    """Проверяет расширение титульного листа: .doc, .docx"""
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext not in ['doc', 'docx']:
        raise ValidationError('Допустимые расширения: doc, docx.')


def validate_antiplagiarism_file(value):
    """Проверяет расширение справки Антиплагиат: .jpg, .pdf"""
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext not in ['jpg', 'pdf']:
        raise ValidationError('Допустимые расширения: jpg, pdf.')


def validate_presentation_file(value):
    """Проверяет расширение презентации: .pptx"""
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext != 'pptx':
        raise ValidationError('Допустимое расширение: pptx.')


def validate_photo_file(value):
    """Проверяет расширение фото эксперта: .jpg, .pdf"""
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext not in ['jpg', 'pdf']:
        raise ValidationError('Допустимые расширения: jpg, pdf.')

def validate_okso_code(value):
    """Проверяет соответствие кода ОКСО маске 00.00.00"""
    if not re.match(r'^\d{2}\.\d{2}\.\d{2}$', value):
        raise ValidationError('Код специальности должен быть в формате 00.00.00')


def validate_file_extension(value, allowed_extensions):
    """Универсальная проверка расширения файла"""
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f'Допустимые расширения: {", ".join(allowed_extensions)}')


# =============================================================================
# Модели секций и расписания
# =============================================================================

class Section(models.Model):
    """Секция форума (номер + название)"""
    number = models.CharField(max_length=10, unique=True, verbose_name='Номер секции')
    name = models.CharField(max_length=200, verbose_name='Название секции')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        ordering = ['number']
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'

    def __str__(self):
        return f"{self.number}. {self.name}"


class Session(models.Model):
    """Конкретная сессия секции (день, время, место)"""
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='sessions', verbose_name='Секция')
    date = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(verbose_name='Начало')
    end_time = models.TimeField(verbose_name='Окончание')
    venue = models.CharField(max_length=255, verbose_name='Площадка (адрес)')
    room = models.CharField(max_length=50, blank=True, verbose_name='Аудитория')
    university = models.CharField(max_length=200, blank=True, verbose_name='ВУЗ-организатор')

    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    def __str__(self):
        return f"{self.section} – {self.date} {self.start_time} ({self.venue})"


# =============================================================================
# Базовый абстрактный класс для общих полей
# =============================================================================

class BasePerson(models.Model):
    """Абстрактная модель с общими полями для всех участников"""
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Пользователь')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    birth_date = models.DateField(verbose_name='Дата рождения')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(unique=True, verbose_name='Email')
    citizenship = models.CharField(max_length=50, blank=True, verbose_name='Гражданство')

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name']


# =============================================================================
# Модель участника (подающего работу)
# =============================================================================

class Participant(BasePerson):
    """Основной участник, подающий конкурсную работу"""
    CATEGORY_CHOICES = [
        ('bachelor', 'Студент Бакалавриата'),
        ('master', 'Студент Магистратуры'),
        ('specialist', 'Студент Специалитета'),
        ('postgraduate', 'Аспирант'),
        ('young_scientist', 'Молодой ученый (до 35 лет)'),
        ('teacher', 'Преподаватель (до 35 лет)'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория участника')
    university = models.CharField(max_length=255, verbose_name='Полное наименование учебного заведения')
    faculty = models.CharField(max_length=255, blank=True, verbose_name='Факультет')
    department = models.CharField(max_length=255, blank=True, verbose_name='Кафедра')
    subdivision = models.CharField(max_length=255, blank=True, verbose_name='Подразделение')
    course = models.CharField(max_length=10, blank=True, verbose_name='Курс')
    okso_code = models.CharField(
        max_length=8,
        validators=[validate_okso_code],
        blank=True,
        verbose_name='Код специальности по ОКСО'
    )

    # Соавторство
    coauthor = models.BooleanField(default=False, verbose_name='В соавторстве')
    coauthor_name = models.CharField(max_length=255, blank=True, verbose_name='ФИО соавтора')
    coauthor_email = models.EmailField(blank=True, verbose_name='Email соавтора')
    coauthor_phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон соавтора')

    # Научный руководитель
    has_supervisor = models.BooleanField(default=False, verbose_name='Наличие научного руководителя')
    supervisor_name = models.CharField(max_length=255, blank=True, verbose_name='ФИО руководителя')
    supervisor_position = models.CharField(max_length=100, blank=True, verbose_name='Должность руководителя')
    supervisor_degree = models.CharField(max_length=50, blank=True, verbose_name='Ученая степень руководителя')
    supervisor_email = models.EmailField(blank=True, verbose_name='Email руководителя')
    supervisor_phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон руководителя')

    no_coauthor_supervisor = models.BooleanField(default=False, verbose_name='Без соавторства и руководителя')

    # Выбранная секция
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, verbose_name='Выбранная секция')

    # Загружаемые файлы с исправленными валидаторами
    work_file = models.FileField(
        upload_to='uploads/works/',
        validators=[validate_work_file],
        verbose_name='Работа'
    )
    title_page = models.FileField(
        upload_to='uploads/title_pages/',
        validators=[validate_title_page_file],
        verbose_name='Титульный лист'
    )
    antiplagiarism_report = models.FileField(
        upload_to='uploads/antiplagiarism/',
        validators=[validate_antiplagiarism_file],
        verbose_name='Справка Антиплагиат'
    )

    # Презентация (только для финалистов)
    presentation_file = models.FileField(
        upload_to='uploads/presentations/',
        validators=[validate_presentation_file],
        blank=True,
        verbose_name='Презентация'
    )


    # Согласия
    consent_personal_data = models.BooleanField(verbose_name='Согласие на обработку персональных данных')
    consent_publication = models.BooleanField(verbose_name='Согласие на публикацию работы на сайте')

    # Поля для финалистов (заполняются, если участник прошёл в финал)
    is_finalist = models.BooleanField(default=False, verbose_name='Финалист')

    # Презентация (только для финалистов)
    presentation_file = models.FileField(
        upload_to='uploads/presentations/',
        validators=[validate_presentation_file],
        blank=True,
        verbose_name='Презентация'
    )

    # Формат участия в финале
    FINAL_FORMAT_CHOICES = [
        ('offline', 'Очно'),
        ('online', 'Онлайн'),
    ]
    final_format = models.CharField(max_length=10, choices=FINAL_FORMAT_CHOICES, blank=True, verbose_name='Формат участия')

    # Выбор конкретной сессии для финала
    chosen_session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Выбранная площадка')

    # Паспортные данные (заполняются только для очного участия)
    passport_series = models.CharField(max_length=4, blank=True, verbose_name='Серия паспорта')
    passport_number = models.CharField(max_length=6, blank=True, verbose_name='Номер паспорта')
    passport_issued_by = models.CharField(max_length=255, blank=True, verbose_name='Кем выдан')
    passport_issued_date = models.DateField(null=True, blank=True, verbose_name='Дата выдачи')
    registration_address = models.TextField(blank=True, verbose_name='Адрес регистрации')

    # Для иностранных граждан (очное участие)
    visa_type = models.CharField(max_length=50, blank=True, verbose_name='Тип визы')
    visa_number = models.CharField(max_length=50, blank=True, verbose_name='Номер визы')
    visa_valid_from = models.DateField(null=True, blank=True, verbose_name='Виза действительна с')
    visa_valid_to = models.DateField(null=True, blank=True, verbose_name='Виза действительна по')
    visa_multiple = models.CharField(max_length=20, blank=True, verbose_name='Кратность визы')
    migration_registration = models.TextField(blank=True, verbose_name='Миграционный учет')

    consent_passport_transfer = models.BooleanField(default=False, verbose_name='Согласие на передачу паспортных данных службе безопасности')

    class Meta:
        verbose_name = 'Участник (с работой)'
        verbose_name_plural = 'Участники (с работами)'

    def __str__(self):
        return f"{self.last_name} {self.first_name} – {self.section}"


# =============================================================================
# Модель эксперта
# =============================================================================

class Expert(BasePerson):
    """Эксперт (член жюри, рецензент)"""
    city = models.CharField(max_length=100, verbose_name='Город')
    work_study_place = models.CharField(max_length=255, verbose_name='Место работы/учебы (организация, должность)')
    education = models.TextField(verbose_name='Образование (включая год окончания и учебное заведение)')
    photo = models.FileField(
        upload_to='uploads/expert_photos/',
        validators=[validate_photo_file],
        verbose_name='Фото'
    )
    academic_degree = models.CharField(max_length=100, blank=True, verbose_name='Ученая степень')
    academic_title = models.CharField(max_length=100, blank=True, verbose_name='Ученое звание')
    professional_profile = models.URLField(blank=True, verbose_name='Ссылка на профессиональный профиль')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Секция')
    work_experience = models.TextField(blank=True, verbose_name='Опыт работы в сфере')
    expert_panel_experience = models.BooleanField(default=False, verbose_name='Опыт участия в экспертных панелях')
    expert_panel_details = models.TextField(blank=True, verbose_name='Подробности опыта')
    ready_for_expert_panel = models.BooleanField(default=False, verbose_name='Готовность участвовать в экспертных панелях')
    confirmation = models.BooleanField(verbose_name='Подтверждение точности данных')
    consent_personal_data = models.BooleanField(verbose_name='Согласие на обработку персональных данных')
    # Captcha обрабатывается на уровне формы

    class Meta:
        verbose_name = 'Эксперт'
        verbose_name_plural = 'Эксперты'

    def __str__(self):
        return f"{self.last_name} {self.first_name} – {self.section or 'без секции'}"


# =============================================================================
# Модель общего участника (СМИ, слушатель и т.п.)
# =============================================================================

class GeneralParticipant(models.Model):
    """Участник без подачи работы (СМИ, слушатель, гость)"""
    STATUS_CHOICES = [
        ('bachelor', 'Студент Бакалавриата'),
        ('master', 'Студент Магистратуры'),
        ('specialist', 'Студент Специалитета'),
        ('postgraduate', 'Аспирант'),
        ('teacher', 'Преподаватель/научный сотрудник'),
        ('manager', 'Руководитель/менеджер'),
        ('entrepreneur', 'Предприниматель'),
        ('media', 'СМИ'),
        ('other', 'Другое'),
    ]
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий (общий интерес)'),
        ('basic', 'Базовый (теоретические знания)'),
        ('advanced', 'Продвинутый (практический опыт)'),
        ('expert', 'Экспертный (профессиональная деятельность)'),
    ]
    GOAL_CHOICES = [
        ('trends', 'Изучение актуальных трендов'),
        ('development', 'Профессиональное развитие'),
        ('networking', 'Знакомство с экспертами и профессионалами отрасли'),
        ('business', 'Поиск бизнес-возможностей'),
        ('academic', 'Академический интерес'),
        ('recruiting', 'Рекрутинг'),
        ('other', 'Другой'),
    ]
    FORMAT_CHOICES = [
        ('offline', 'Очное участие'),
        ('online', 'Онлайн участие'),
    ]

    # Личные данные
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    work_study = models.CharField(max_length=255, verbose_name='Место работы/учебы')

    # Статус
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус участника')
    other_status = models.CharField(max_length=100, blank=True, verbose_name='Другое (статус)')

    # Для СМИ – поле-индикатор, требующее аккредитации (логика в представлениях)
    is_media = models.BooleanField(default=False, verbose_name='СМИ')

    # Интересы
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, verbose_name='Интересующая секция')
    preparation_level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name='Уровень подготовки по тематике')

    # Цели (многие ко многим, так как можно выбрать несколько)
    goals = models.ManyToManyField('Goal', blank=True, verbose_name='Цели участия')
    other_goal = models.CharField(max_length=200, blank=True, verbose_name='Другая цель')

    # Формат участия
    format_participation = models.CharField(max_length=10, choices=FORMAT_CHOICES, verbose_name='Формат участия')

    # Для очного формата – паспортные и визовые данные
    # (аналогично Participant)
    citizenship = models.CharField(max_length=50, blank=True, verbose_name='Гражданство')
    passport_series = models.CharField(max_length=4, blank=True, verbose_name='Серия паспорта')
    passport_number = models.CharField(max_length=6, blank=True, verbose_name='Номер паспорта')
    passport_issued_by = models.CharField(max_length=255, blank=True, verbose_name='Кем выдан')
    passport_issued_date = models.DateField(null=True, blank=True, verbose_name='Дата выдачи')
    registration_address = models.TextField(blank=True, verbose_name='Адрес регистрации')
    visa_type = models.CharField(max_length=50, blank=True, verbose_name='Тип визы')
    visa_number = models.CharField(max_length=50, blank=True, verbose_name='Номер визы')
    visa_valid_from = models.DateField(null=True, blank=True, verbose_name='Виза действительна с')
    visa_valid_to = models.DateField(null=True, blank=True, verbose_name='Виза действительна по')
    visa_multiple = models.CharField(max_length=20, blank=True, verbose_name='Кратность визы')
    migration_registration = models.TextField(blank=True, verbose_name='Миграционный учет')
    work_university = models.CharField(max_length=255, blank=True, verbose_name='ВУЗ/место работы')

    consent_passport_transfer = models.BooleanField(default=False, verbose_name='Согласие на передачу паспортных данных службе безопасности')
    consent_personal_data = models.BooleanField(verbose_name='Согласие на обработку персональных данных')

    class Meta:
        verbose_name = 'Общий участник'
        verbose_name_plural = 'Общие участники'

    def __str__(self):
        return f"{self.last_name} {self.first_name} – {self.get_status_display()}"


class Goal(models.Model):
    """Модель для целей участия (выбор из списка или свой вариант)"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название цели')

    class Meta:
        verbose_name = 'Цель участия'
        verbose_name_plural = 'Цели участия'

    def __str__(self):
        return self.name