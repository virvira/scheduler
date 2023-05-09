from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import GoalCategory, Goal, Status
from todolist import settings
import os

states = {}

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                if item.message:
                    self.handle_message(item.message)
                else:
                    self.handle_message(item.edited_message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)
        if tg_user.user:
            self.handle_authorized(tg_user, msg)
        else:
            self.handle_unauthorized(tg_user, msg)

    def handle_unauthorized(self, tg_user: TgUser, msg: Message):
        self.tg_client.send_message(msg.chat.id, 'Подтвердите, пожалуйста, свой аккаунт')
        code = os.urandom(12).hex()
        tg_user.verification_code = code
        tg_user.save(update_fields=['verification_code'])
        self.tg_client.send_message(tg_user.chat_id, f'Код верификации: {code}')

    def handle_authorized(self, tg_user: TgUser, msg: Message):
        allowed_commands = ['/goals', '/create', '/cancel']
        if msg.text in allowed_commands:
            self.handle_command(tg_user, msg)
        elif ('user' not in states) and (msg.text not in allowed_commands):
            self.tg_client.send_message(tg_user.chat_id, 'Такой команды не существует')
        elif (msg.text not in allowed_commands) and (states['user']) and \
             ('category' not in states):
            category = self.handle_save_category(tg_user, msg.text)
            if category:
                states['category'] = category
                self.tg_client.send_message(tg_user.chat_id, f'Выбрана категория {category.title}')
        elif (msg.text not in allowed_commands) and (states['user']) and \
                (states['category']) and ('goal_title' not in states):
            states['goal_title'] = msg.text
            goal = Goal.objects.create(title=states['goal_title'],
                                       user=states['user'],
                                       category=states['category'])
            self.tg_client.send_message(tg_user.chat_id, f'Цель {goal} создана')
            del states['user']
            del states['category']
            del states['goal_title']

    def handle_command(self, tg_user: TgUser, msg: Message):
        match msg.text:
            case '/goals':
                self.get_goals(tg_user)
            case '/create':
                self.handle_categories(tg_user)
            case '/cancel':
                self.get_cancel(tg_user)

    def get_goals(self, tg_user: TgUser):
        goals = Goal.objects.filter(
            category__board__participants__user=tg_user.user
        ).exclude(status=Status.archived)
        if not goals:
            self.tg_client.send_message('Цели не найдены')
        else:
            resp = '\n'.join([goal.title for goal in goals])
            self.tg_client.send_message(tg_user.chat_id, resp)

    def handle_categories(self, tg_user: TgUser):
        categories = GoalCategory.objects.filter(board__participants__user=tg_user.user, is_deleted=False)

        if not categories:
            self.tg_client.send_message(tg_user.chat_id, 'Категории не найдены')
        else:
            resp = '\n'.join([f'{cat.id}: {cat.title}' for cat in categories])
            self.tg_client.send_message(tg_user.chat_id, 'Выберите номер категории для новой цели')
            self.tg_client.send_message(tg_user.chat_id, resp)
            if 'user' not in states:
                states['user'] = tg_user.user

    def handle_save_category(self, tg_user: TgUser, msg: str):
        category_id = int(msg)
        category_data = GoalCategory.objects.filter(user=tg_user.user).get(pk=category_id)
        return category_data

    def get_cancel(self, tg_user: TgUser):
        if 'user' in states:
            del states['user']
        if 'category' in states:
            del states['category']
        if 'goal_title' in states:
            del states['goal_title']
        self.tg_client.send_message(tg_user.chat_id, 'Отмена')
