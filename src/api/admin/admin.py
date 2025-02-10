from sqladmin import Admin, BaseView, expose
from starlette.requests import Request
from starlette.responses import RedirectResponse

from api.admin.views.job import JobAdmin
from api.admin.views.user import UserAdmin


class AdminHome(BaseView):
    name = ""

    @expose("/", methods=["GET"])
    async def test_page(self, request: Request) -> RedirectResponse:
        return RedirectResponse("/admin/")


def load_admin_site(admin: Admin) -> None:
    admin.add_view(UserAdmin)
    admin.add_view(JobAdmin)
    admin.add_base_view(AdminHome)
