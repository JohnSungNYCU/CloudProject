# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from common.models import BaseModel
from systems.models import *
from tools.models import Upload



class WorkflowType(BaseModel):
    name = models.CharField('名稱', max_length=50)
    status = models.BooleanField(default=True)
    code = models.CharField(max_length=32, unique=True, verbose_name='代碼')
    order_id = models.IntegerField('狀態順序', default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order_id']
        verbose_name = '工作流類型'
        verbose_name_plural = verbose_name


class Workflow(BaseModel):
    """
    工作流
    """
    name = models.CharField('名稱', max_length=50)
    key = models.CharField('流程標識key', blank=True, max_length=168)
    ticket_sn_prefix = models.CharField('工單流水號前綴', default='xxoo', max_length=20)
    status = models.BooleanField(default=True)
    type = models.ForeignKey(WorkflowType, on_delete=models.CASCADE, verbose_name='工作流類型')
    roles = models.ManyToManyField(Role, verbose_name='關聯角色', blank=True, related_name="workflow_set", related_query_name="workflow")
    view_permission_check = models.BooleanField('查看權限校驗', default=True, help_text='開啟後，只允許工單的關聯人(創建人、曾經的處理人)有權限查看工單')
    limit_expression = models.TextField('限制表達式', default='{}', blank=True,
                                        help_text='限制週期({"period":24} 24小時), 限制次數({"count":1}在限制週期內只允許提交1次), 限制級別({"level":1} 針對(1單個用戶 2全局)限制週期限制次數,默認特定用戶);允許特定人員提交({"allow_persons":"zhangsan,lisi"}只允許張三提交工單,{"allow_depts":"1,2"}只允許部門id為1和2的用戶提交工單，{"allow_roles":"1,2"}只允許角色id為1和2的用戶提交工單)')
    display_form_str = models.TextField('展現表單字段', default='[]', blank=True,
                                        help_text='默認"[]"，用於用戶只有對應工單查看權限時顯示哪些字段,field_key的list的json,如["days","sn"],內置特殊字段participant_info.participant_name:當前處理人信息(部門名稱、角色名稱)，state.state_name:當前狀態的狀態名,workflow.workflow_name:工作流名稱')
    title_template = models.CharField('標題模板', max_length=50, default='你有一個待辦工單:{title}', null=True, blank=True,
                                      help_text='工單字段的值可以作為參數寫到模板中，格式如：你有一個待辦工單:{title}')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工作流'
        verbose_name_plural = verbose_name


field_type = {
    1: '字符串',
    2: '整型',
    3: '浮點型',
    4: '布爾',
    5: '日期',
    6: '日期時間',
    7: '範圍日期',
    8: '文本域',
    9: '單選框',
    10: '下拉列表',
    11: '用戶名',
    12: '多選框',
    13: '多選下拉',
    14: '多選用戶名',
    15: '文件上傳',
}


class CustomField(BaseModel):
    """自定義字段, 設定某個工作流有哪些自定義字段"""
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='工作流')
    field_attribute = models.BooleanField('字段是否內置', default=False)
    field_type = models.CharField(max_length=1, choices=tuple(field_type.items()), default=0, verbose_name='字段類型')
    field_key = models.CharField('字段標識', max_length=50, help_text='字段類型請儘量特殊，避免與系統中關鍵字衝突')
    field_name = models.CharField('字段名稱', max_length=50)
    # 內置 field 的 order_id 不要超過10
    order_id = models.IntegerField('排序', default=0)
    default_value = models.CharField('默認值', null=True, blank=True, max_length=100, help_text='前端展示時，可以將此內容作為表單中的該字段的默認值')
    field_template = models.TextField('文本域模板', default='', blank=True, help_text='文本域類型字段前端顯示時可以將此內容作為字段的placeholder')
    boolean_field_display = models.CharField('布爾類型顯示名', max_length=100, default='{}', blank=True,
                                             help_text='當為布爾類型時候，可以支持自定義顯示形式。{"1":"是","0":"否"}或{"1":"需要","0":"不需要"}，注意數字也需要引號')
    field_choice = models.CharField('radio、checkbox、select的選項', max_length=255, default='{}', blank=True,
                                    help_text='radio,checkbox,select,multiselect類型可供選擇的選項，格式為json如:{"1":"中國", "2":"美國"},注意數字也需要引號')
    label = models.CharField('標籤', max_length=100, blank=True, default='{}',
                             help_text='自定義標籤，json格式，調用方可根據標籤自行處理特殊場景邏輯，loonflow只保存文本內容')
    upload = models.ForeignKey(Upload, on_delete=models.SET_NULL, null=True, blank=True, related_name='custom_fields')
    

    def __str__(self):
        return self.field_name

    class Meta:
        ordering = ['order_id']
        verbose_name = '工作流自定義字段'
        verbose_name_plural = verbose_name


# 0.普通類型 1.初始狀態(用於新建工單時,獲取對應的字段必填及transition信息) 2.結束狀態(此狀態下的工單不得再處理，即沒有對應的transition)
state_type = {
    0: '普通狀態',
    1: '初始狀態',
    2: '結束狀態',
}

participant_type = {
    'none': '無處理人',
    'user': '個人',
    'group': '部門',
    'role': '角色',
}


class State(BaseModel):
    """
    狀態記錄, 變量支持通過腳本獲取
    """
    name = models.CharField('名稱', max_length=50)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='工作流')
    is_hidden = models.BooleanField('是否隱藏', default=False, help_text='設置為True時,獲取工單步驟api中不顯示此狀態(當前處於此狀態時除外)')
    order_id = models.IntegerField('狀態順序', default=1)
    state_type = models.CharField(max_length=1, choices=tuple(state_type.items()), default=0, verbose_name='狀態類型')
    enable_retreat = models.BooleanField('允許撤回', default=False, help_text='開啟後允許工單創建人在此狀態直接撤回工單到初始狀態')
    participant_type = models.CharField(max_length=5, choices=tuple(participant_type.items()), default='none', verbose_name='參與者類型')
    user_participant = models.ManyToManyField(User, blank=True, verbose_name='參與用戶')
    group_participant = models.ManyToManyField(Group, blank=True, verbose_name='參與組')
    role_participant = models.ManyToManyField(Role, blank=True, verbose_name='參與角色')
    fields = models.ManyToManyField(CustomField, blank=True, verbose_name='可編輯字段')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order_id']
        verbose_name = '工作流狀態'
        verbose_name_plural = verbose_name


transition_name = {
    0: '保存',
    1: '轉交下一步',
    2: '駁回',
    3: '撤銷',
    4: '關閉',
}

transition_type = {
    0: '常規流轉',
    1: '定時器流轉',
}

attribute_type = {
    0: '草稿',
    1: '待審',
    2: '駁回',
    3: '撤銷',
    4: '結束',
    5: '已關閉',
}


class Transition(BaseModel):
    """
    工作流流轉，定時器，條件(允許跳過)， 條件流轉與定時器不可同時存在
    """
    name = models.CharField('名稱類型', max_length=1, choices=tuple(transition_name.items()), default=1)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='工作流')
    transition_type = models.CharField('流轉類型', max_length=1, choices=tuple(transition_type.items()), default=0)
    timer = models.IntegerField('定時器(單位秒)', default=0, help_text='流轉類型設置為定時器流轉時生效,單位秒。處於源狀態X秒後如果狀態都沒有過變化則自動流轉到目標狀態')
    source_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL, related_name="source_state", verbose_name='源狀態')
    dest_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL, related_name="dest_state", verbose_name='目的狀態')
    condition_expression = models.TextField('條件表達式', default='[]',
                                            help_text='流轉條件表達式，根據表達式中的條件來確定流轉的下個狀態，格式為[{"expression":"{days} > 3 and {days}<10", "target_state_id":11}] 其中{}用於填充工單的字段key,運算時會換算成實際的值，當符合條件下個狀態將變為target_state_id中的值,表達式只支持簡單的運算或datetime/time運算.loonflow會以首次匹配成功的條件為準，所以多個條件不要有衝突')
    attribute_type = models.CharField(max_length=1, choices=tuple(attribute_type.items()), default=0, verbose_name='屬性類型')
    alert_enable = models.BooleanField('點擊彈窗提示', default=False)
    alert_text = models.CharField('彈窗內容', max_length=100, default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工作流流轉'
        verbose_name_plural = verbose_name


"""
https://github.com/GoldSubmarine/workflow-bpmn-modeler
https://github.com/miyuesc/bpmn-process-designer
https://juejin.cn/post/6844904069736169480
"""


class WorkflowBpmn(BaseModel):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='工作流')
    xml = models.TextField('xml數據', blank=True)
    svg = models.TextField('svg數據', blank=True)

    class Meta:
        verbose_name = '工作流bpmn'
        verbose_name_plural = verbose_name
