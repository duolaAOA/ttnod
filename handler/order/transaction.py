# -*-coding:utf-8 -*-


import time
from handler.routes import Route
from ..base import BaseHandler


@Route('/')
@Route('/(?P<page>\d*)')
class IndexHandler(BaseHandler):
    """
    total_amount:   历史总金额 amount
    total_score:    历史总积分 score
    a_week_total_amount      一周内总金额
    a_week_total_score       一周内总积分
    """

    def get(self, page: int):
        specify_time = False
        page = self.get_argument("page", 1)

        recharge_total_amount = ''
        recharge_total_score = ''
        recharge_total_count = ''
        score_total_score = ''
        score_total_count = ''
        recharge_week_total_amount = ''
        recharge_week_total_score = ''
        recharge_week_total_count = ''
        score_week_total_score = ''
        score_week_total_count = ''

        recharge_total_obj = self.mongdb_db.get_aggregate_recharges()
        for obj in recharge_total_obj:
            recharge_total_amount = obj.get("recharge_total_amount", "")
            recharge_total_score = obj.get("recharge_total_score", "")
            recharge_total_count = obj.get("recharge_total_count", 0)

        score_total_obj = self.mongdb_db.get_aggregate_scores()
        for obj in score_total_obj:
            score_total_score = obj.get("score_total_score", "")
            score_total_count = obj.get("score_total_count", 0)

        recharge_week_obj = self.mongdb_db.get_week_aggregate_recharges()
        for obj in recharge_week_obj:
            recharge_week_total_amount = obj.get("recharge_week_total_amount", "")
            recharge_week_total_score = obj.get("recharge_week_total_score", "")
            recharge_week_total_count = obj.get("recharge_week_total_count", 0)

        score_week_obj = self.mongdb_db.get_week_aggregate_scores()
        for obj in score_week_obj:
            score_week_total_score = obj.get("score_week_total_score", "")
            score_week_total_count = obj.get("score_week_total_count", 0)

        week_recharge_record_obj = self.mongdb_db.get_week_recharge_record(page=int(page))    # 近一周充值记录

        kwargs = dict(recharge_total_amount=recharge_total_amount,
                      recharge_total_score=recharge_total_score,
                      recharge_total_count=recharge_total_count,
                      score_total_score=score_total_score,
                      score_total_count=score_total_count,
                      recharge_week_total_amount=recharge_week_total_amount,
                      recharge_week_total_score=recharge_week_total_score,
                      recharge_week_total_count=recharge_week_total_count,
                      score_week_total_score=score_week_total_score,
                      score_week_total_count=score_week_total_count, week_recharge_record_obj=week_recharge_record_obj,
                      specify_time=specify_time)

        self.render('index.html', **kwargs)

    def post(self, *args, **kwargs):
        specify_time = self.get_argument("datetime")
        if not specify_time:
            specify_time = time.strftime("%Y-%m-%d")

        recharge_total_obj = self.mongdb_db.get_aggregate_recharges()
        for obj in recharge_total_obj:
            recharge_total_amount = obj.get("recharge_total_amount", "")
            recharge_total_score = obj.get("recharge_total_score", "")
            recharge_total_count = obj.get("recharge_total_count", 0)

        score_total_obj = self.mongdb_db.get_aggregate_scores()
        for obj in score_total_obj:
            score_total_score = obj.get("score_total_score", "")
            score_total_count = obj.get("score_total_count", 0)

        recharge_specify_obj = self.mongdb_db.get_specify_datetime_recharges(specify_datetime=specify_time)
        recharge_specify_total_amount = ''
        recharge_specify_total_score = ''
        recharge_specify_total_count = ''
        score_specify_total_score = ''
        score_specify_total_count = ''
        for obj in recharge_specify_obj:
            recharge_specify_total_amount = obj.get("recharge_specify_total_amount", "")
            recharge_specify_total_score = obj.get("recharge_specify_total_score", "")
            recharge_specify_total_count = obj.get("recharge_specify_total_count", 0)

        score_specify_obj = self.mongdb_db.get_specify_datetime_scores(specify_datetime=specify_time)
        for obj in score_specify_obj:
            score_specify_total_score = obj.get("score_specify_total_score", "")
            score_specify_total_count = obj.get("score_specify_total_count", 0)

        specify_recharge_record_obj = self.mongdb_db.get_recharge_specify_datetime_record(specify_datetime=specify_time)

        kwargs = dict(
            recharge_total_amount=recharge_total_amount,
            recharge_total_score=recharge_total_score,
            recharge_total_count=recharge_total_count,
            score_total_score=score_total_score,
            score_total_count=score_total_count,

            recharge_week_total_amount=recharge_specify_total_amount,
            recharge_week_total_score=recharge_specify_total_score,
            recharge_week_total_count=recharge_specify_total_count,

            score_week_total_score=score_specify_total_score,
            score_week_total_count=score_specify_total_count,

            week_recharge_record_obj=specify_recharge_record_obj,
            specify_time=specify_time
        )
        self.render('index.html', **kwargs)
