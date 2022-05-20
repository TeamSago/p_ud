from django.shortcuts import render, redirect
from .forms import BoardWriteForm
from .models import Board
from users.models import User
from users.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta

# Create your views here.
def board_list(request):
    login_session = request.session.get("login_session", "")
    context = {"login_session": login_session}

    py_boards = Board.objects.filter(board_name="Python")
    js_boards = Board.objects.filter(board_name="JavaScript")

    context["py_boards"] = py_boards
    context["js_boards"] = js_boards
    return render(request, "board/board_list.html", context)


@login_required
def board_write(request):
    login_session = request.session.get("login_session", "")
    context = {"login_session": login_session}

    if request.method == "GET":
        write_form = BoardWriteForm()
        context["forms"] = write_form
        return render(request, "board/board_write.html", context)

    elif request.method == "POST":
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            writer = User.objects.get(user_id=login_session)
            board = Board(
                title=write_form.title,
                contents=write_form.contents,
                writer=writer,
                board_name=write_form.board_name,
            )
            board.save()
            return redirect("/board")
        else:
            context["forms"] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context["error"] = value
            return render(request, "board/board_write.html", context)


def board_detail(request, pk):
    login_session = request.session.get("login_session", "")
    context = {"login_session": login_session}

    board = get_object_or_404(Board, id=pk)
    context["board"] = board

    # 글쓴이인지 확인
    if board.writer.user_id == login_session:
        context["writer"] = True
    else:
        context["writer"] = False

    # 조회수 기능(쿠키이용)
    expire_date, now = datetime.now(), datetime().now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replacae(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_second()

    cookie_value = request.COOKIES.get("hitboard", "_")

    if f"_{pk}_" not in cookie_value:
        cookie_value += f"{pk}_"
        response.set_cookie(
            "hitboard", value=cookie_value, max_age=max_age, httponly=True
        )
        board.hits += 1
        board.save()
    return response

    return render(request, "board/board_detail.html", context)


def board_delete(request, pk):
    login_session = request.session.get("login_session", "")
    board = get_object_or_404(Board, id=pk)
    if board.writer.user_id == login_session:
        board.delete()
        return redirect("/board")
    else:
        return redirect(f"/board/detail/{pk}/")


@login_required
def board_modify(request, pk):
    login_session = request.session.get("login_session", "")
    context = {"login_session": login_session}

    board = get_object_or_404(Board, id=pk)
    context["board"] = board

    if board.writer.user_id != login_session:
        return redirect(f"/board/detail/{pk}/")

    if request.method == "GET":
        write_form = BoardWriteForm(instance=board)
        context["forms"] = write_form
        return render(request, "board/board_modify.html", context)

    elif request.method == "POST":
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            board.title = write_form.title
            board.contents = write_form.contents
            board.board_name = write_form.board_name

            board.save()
            return redirect("/board")
        else:
            context["forms"] = write_form
            if write_form.errors:
                for value in write_form.errors.value():
                    context["error"] = value

            return render(request, "board/board_modify.html", context)
