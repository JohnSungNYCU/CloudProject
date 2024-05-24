# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password

from workflows.models import *
from systems.models import *


class Command(BaseCommand):
    help = '假期工作流'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('############ 配置工作流用戶角色 ###########'))
        topgroup = Group.objects.get(name='top', code='top')

        group_fab = Group.objects.create(name='Fab', code='fab', sequence=1, parent=topgroup)
        group_lab = Group.objects.create(name='Lab', code='lab', sequence=2, parent=topgroup)
        group_manager = Group.objects.create(name='經理', code='manager', sequence=3, parent=topgroup)

        self.stdout.write(self.style.SUCCESS('############ 初始化角色 ###########'))
        toprole = Role.objects.get(name='top', code='top')

        role_fab_tl = Role.objects.create(name='Fab經理', code='fab_tl', sequence=1, group=group_manager, parent=toprole)
        role_fab = Role.objects.create(name='Fab', code='fab', sequence=1, group=group_fab, parent=toprole)
        role_lab_tl = Role.objects.create(name='Lab經理', code='lab_tl', sequence=2, group=group_manager, parent=toprole)
        role_lab = Role.objects.create(name='Lab', code='lab', sequence=2, group=group_lab, parent=toprole)

        self.stdout.write(self.style.SUCCESS('############ 初始化用戶 ###########'))

        fab_tl_1 = User.objects.create(username='Fab_tl_1', password=make_password("123456"), realname="Fab_tl_1", group=group_manager)
        fab_tl_1.roles.add(role_fab_tl)
        fab_tl_2 = User.objects.create(username='Fab_tl_2', password=make_password("123456"), realname="Fab_tl_2", group=group_manager)
        fab_tl_2.roles.add(role_fab_tl)
        fab1 = User.objects.create(username='FabA', password=make_password("123456"), realname="Fab-A", group=group_fab)
        fab1.roles.add(role_fab)
        fab2 = User.objects.create(username='FabB', password=make_password("123456"), realname="Fab-B", group=group_fab)
        fab2.roles.add(role_fab)
        fab3 = User.objects.create(username='FabC', password=make_password("123456"), realname="FAB-C", group=group_fab)
        fab3.roles.add(role_fab)
        
        lab_tl_1 = User.objects.create(username='Lab_tl_1', password=make_password("123456"), realname="Lab_tl_1", group=group_manager)
        lab_tl_1.roles.add(role_lab_tl)
        lab_tl_2 = User.objects.create(username='Lab_tl_2', password=make_password("123456"), realname="Lab_tl_2", group=group_manager)
        lab_tl_2.roles.add(role_lab_tl)
        lab1 = User.objects.create(username='LabA', password=make_password("123456"), realname="化學實驗室", group=group_lab)
        lab1.roles.add(role_lab)
        lab2 = User.objects.create(username='LabB', password=make_password("123456"), realname="表面分析實驗室", group=group_lab)
        lab2.roles.add(role_lab)
        lab3 = User.objects.create(username='LabC', password=make_password("123456"), realname="成分分析實驗室", group=group_lab)
        lab3.roles.add(role_lab)

        self.stdout.write(self.style.SUCCESS('############ 發布工作流 ###########'))
        ## 工作流类型
        it_type_1 = WorkflowType.objects.create(name='Lab', code='it_1', order_id=1)

        ## 工作流
        lab_wf = Workflow.objects.create(name='工單', type=it_type_1, ticket_sn_prefix='deploy')

        ## 工作流字段
        # 建立内置字段
        CustomField.objects.create(field_name="申請人", order_id=1, field_attribute=True, field_type=1,
                                   field_key="create_user", workflow=lab_wf)
        CustomField.objects.create(field_name="申請時間", order_id=2, field_attribute=True, field_type=6,
                                   field_key="create_time", workflow=lab_wf)
        CustomField.objects.create(field_name="部門", order_id=3, field_attribute=True, field_type=1, field_key="group",
                                   workflow=lab_wf)
        CustomField.objects.create(field_name="工號", order_id=4, field_attribute=True, field_type=2, field_key="id",
                                   workflow=lab_wf)
        # 建立扩展字段
        c0 = CustomField.objects.create(field_name="急件狀態", order_id=40, field_type=9, field_key="status", field_choice='{"1":"一般"}', workflow=lab_wf)
        c1 = CustomField.objects.create(field_name="截止時間", order_id=10, field_type=6, field_key="start_time",
                                        workflow=lab_wf)
        c2 = CustomField.objects.create(field_name="檢測項目", order_id=30, field_type=9, field_key="type",
                                        field_choice='{"1":"晶圓檢測與分析", "2":"材料分析", "3": "其他"}', workflow=lab_wf)
        c3 = CustomField.objects.create(field_name="comment", order_id=50, field_type=8, field_key="memo",
                                        workflow=lab_wf)
        c4 = CustomField.objects.create(field_name="經理審核", order_id=60, field_type=9, field_key="leader_radio",
                                        field_choice='{"1":"同意", "2":"不同意"}', workflow=lab_wf)
        c5 = CustomField.objects.create(field_name="進行測試", order_id=80, field_type=9, field_key="ops_radio",
                                        field_choice='{"1":"已執行", "2":"未執行"}', workflow=lab_wf)

        # 建立初始和结束状态
        s1 = State.objects.create(name="開始", order_id=1, state_type=1, is_hidden=True, participant_type='none',
                                  workflow=lab_wf)
        s2 = State.objects.create(name="關閉", order_id=99, state_type=2, is_hidden=True, participant_type='none',
                                  workflow=lab_wf)
        # 建立流转状态
        s3 = State.objects.create(name="申請人-編輯中", order_id=2, participant_type='none', workflow=lab_wf)
        s3.fields.add(c0, c1, c2, c3)
        s4 = State.objects.create(name="經理-審批中", order_id=3, participant_type='role', workflow=lab_wf)
        s4.fields.add(c4)
        s4.role_participant.add(role_lab_tl)
        s5 = State.objects.create(name="測試-執行中", order_id=4, participant_type='role', workflow=lab_wf)
        s5.fields.add(c5)
        s5.role_participant.add(role_fab)
        s6 = State.objects.create(name="結束", order_id=98, state_type=2, participant_type='none', workflow=lab_wf)

        # 建立工作流步骤
        Transition.objects.create(name=0, source_state=s1, dest_state=s3, attribute_type=0, workflow=lab_wf)
        Transition.objects.create(name=1, source_state=s1, dest_state=s4, attribute_type=1, workflow=lab_wf)

        Transition.objects.create(name=0, source_state=s3, dest_state=s3, attribute_type=0, workflow=lab_wf)
        Transition.objects.create(name=1, source_state=s3, dest_state=s4, attribute_type=1, workflow=lab_wf)
        Transition.objects.create(name=3, source_state=s3, dest_state=s6, attribute_type=3, workflow=lab_wf)

        Transition.objects.create(name=2, source_state=s4, dest_state=s3, attribute_type=2, workflow=lab_wf)
        Transition.objects.create(name=1, source_state=s4, dest_state=s5, attribute_type=1, workflow=lab_wf)

        Transition.objects.create(name=2, source_state=s5, dest_state=s3, attribute_type=2, workflow=lab_wf)
        Transition.objects.create(name=4, source_state=s5, dest_state=s2, attribute_type=5, workflow=lab_wf)

        self.stdout.write(self.style.SUCCESS('############ 初始化角色權限 ###########'))
        menus = [34, 35, 36, 37, 38, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76,
                 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96]
        perms = [52, 56, 60, 92, 96, 48, 44, 52, 73, 74, 75, 76, 85, 86, 87, 88, 81, 82, 83, 84, 77, 78, 79, 80, 28, 32, 68, 64]
        menu_obj_list = Menu.objects.filter(id__in=menus)
        perm_obj_list = Permission.objects.filter(id__in=perms)

        role_fab_tl.menus.add(*menu_obj_list)
        role_fab_tl.model_perms.add(*perm_obj_list)
        role_fab.menus.add(*menu_obj_list)
        role_fab.model_perms.add(*perm_obj_list)
        role_lab_tl.menus.add(*menu_obj_list)
        role_lab_tl.model_perms.add(*perm_obj_list)
        role_lab.menus.add(*menu_obj_list)
        role_lab.model_perms.add(*perm_obj_list)
        self.stdout.write(self.style.SUCCESS('發布工作流完成'))

        self.stdout.write(self.style.SUCCESS('############ 發布工作流 ###########'))
        ## 工作流类型
        it_type_2 = WorkflowType.objects.create(name='Fab', code='it_2', order_id=2)

        ## 工作流
        fab_wf = Workflow.objects.create(name='委託單', type=it_type_2, ticket_sn_prefix='deploy')

        ## 工作流字段
        # 建立内置字段
        CustomField.objects.create(field_name="申請人", order_id=1, field_attribute=True, field_type=1,
                                   field_key="create_user", workflow=fab_wf)
        CustomField.objects.create(field_name="申請時間", order_id=2, field_attribute=True, field_type=6,
                                   field_key="create_time", workflow=fab_wf)
        CustomField.objects.create(field_name="部門", order_id=3, field_attribute=True, field_type=1, field_key="group",
                                   workflow=fab_wf)
        CustomField.objects.create(field_name="工號", order_id=4, field_attribute=True, field_type=2, field_key="id",
                                   workflow=fab_wf)
        # 建立扩展字段
        c1 = CustomField.objects.create(field_name="截止時間", order_id=10, field_type=6, field_key="start_time",
                                        workflow=fab_wf)
        c2 = CustomField.objects.create(field_name="檢測項目", order_id=30, field_type=9, field_key="type",
                                        field_choice='{"1":"FTIR測試", "2":"ICP-MS測試", "3": "其他"}', workflow=fab_wf)
        c3 = CustomField.objects.create(field_name="急件狀態", order_id=40, field_type=9, field_key="status",
                                        field_choice='{"1":"一般", "2":"急單", "3": "特急單"}', workflow=fab_wf)
        c4 = CustomField.objects.create(field_name="comment", order_id=50, field_type=8, field_key="memo",
                                        workflow=fab_wf)
        c5 = CustomField.objects.create(field_name="經理審核", order_id=60, field_type=9, field_key="leader_radio",
                                        field_choice='{"1":"同意", "2":"不同意"}', workflow=fab_wf)
        c6 = CustomField.objects.create(field_name="進行測試", order_id=80, field_type=9, field_key="ops_radio",
                                        field_choice='{"1":"已執行", "2":"未執行"}', workflow=fab_wf)

        # 建立初始和结束状态
        s1 = State.objects.create(name="開始", order_id=1, state_type=1, is_hidden=True, participant_type='none',
                                  workflow=fab_wf)
        s2 = State.objects.create(name="關閉", order_id=99, state_type=2, is_hidden=True, participant_type='none',
                                  workflow=fab_wf)
        # 建立流转状态
        s3 = State.objects.create(name="申請人-編輯中", order_id=2, participant_type='none', workflow=fab_wf)
        s3.fields.add(c1, c2, c3, c4)
        s4 = State.objects.create(name="經理-審批中", order_id=3, participant_type='role', workflow=fab_wf)
        s4.fields.add(c5)
        s4.role_participant.add(role_fab_tl)
        s5 = State.objects.create(name="測試-執行中", order_id=4, participant_type='role', workflow=fab_wf)
        s5.fields.add(c6)
        s5.role_participant.add(role_lab)
        s6 = State.objects.create(name="結束", order_id=98, state_type=2, participant_type='none', workflow=fab_wf)

        # 建立工作流步骤
        Transition.objects.create(name=0, source_state=s1, dest_state=s3, attribute_type=0, workflow=fab_wf)
        Transition.objects.create(name=1, source_state=s1, dest_state=s4, attribute_type=1, workflow=fab_wf)

        Transition.objects.create(name=0, source_state=s3, dest_state=s3, attribute_type=0, workflow=fab_wf)
        Transition.objects.create(name=1, source_state=s3, dest_state=s4, attribute_type=1, workflow=fab_wf)
        Transition.objects.create(name=3, source_state=s3, dest_state=s6, attribute_type=3, workflow=fab_wf)

        Transition.objects.create(name=2, source_state=s4, dest_state=s3, attribute_type=2, workflow=fab_wf)
        Transition.objects.create(name=1, source_state=s4, dest_state=s5, attribute_type=1, workflow=fab_wf)

        Transition.objects.create(name=2, source_state=s5, dest_state=s3, attribute_type=2, workflow=fab_wf)
        Transition.objects.create(name=4, source_state=s5, dest_state=s2, attribute_type=5, workflow=fab_wf)

        self.stdout.write(self.style.SUCCESS('發布工作流完成'))
