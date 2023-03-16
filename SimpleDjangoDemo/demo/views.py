from django.views.generic.base import TemplateView
# from django.views import View
# from django.http import HttpResponse
from demo.dbutils import counterparties_sql as cp
from demo.dbutils.counterparties_sql import cn


# class Home(View):
#
#     def get(self, request, *args, **kwargs):
#         f = open(r'demo/templates/flatpages/default.html', 'r')
#         pattern = f.read()
#         f.close()
#         return HttpResponse(pattern + "Добро пожаловать на первый тестовый проект Django")


class CounterpartiesTable(TemplateView):
    template_name = 'flatpages/counterparties.html'

    def get_context_data(self, **kwargs):
        ctx = super(CounterpartiesTable, self).get_context_data(**kwargs)
        ctx['header'] = ['#', 'Name', 'Begin date']
        rows = cp.select_all_counterparties(cn)
        ctx['rows'] = []
        for row in rows:
            ctx['rows'].append({'id': row[0], 'Name': row[1], 'Begin_date': row[2]})
        # cp.exec_command(cn, "INSERT INTO COUNTERPARTIES values(1, 'AbsolutBank', '01.01.2023', null)")
        cn.rollback()
        return ctx
