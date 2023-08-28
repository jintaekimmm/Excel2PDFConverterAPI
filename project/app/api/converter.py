import os
import asyncio
from urllib.parse import quote

from fastapi import APIRouter, status, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from loguru import logger

from utils.command import PDF_CONV_COMMAND, PDF_CONV_COMMAND_TIMEOUT

router = APIRouter(prefix="/e2p", tags=["converter"])


@router.post("/conv")
async def excel_to_pdf_convert_api(
    *,
    file: UploadFile = File(...),
):
    """
    libreoffice의 'localc' 명령어를 통해 excel 파일을 pdf로 변환한다
    변환이 완료된 pdf 파일을 반환한다
    """

    new_filename = f"{file.filename}"
    # 확장자를 제거한다
    new_filename, _ = os.path.splitext(new_filename)
    # 변환되어 저장될 파일 이름
    saved_pdf = f"{new_filename}.pdf"

    try:
        with open(new_filename, "wb") as f:
            f.write(await file.read())

        EXTENSION = "pdf"
        cmd = PDF_CONV_COMMAND.format(extension=EXTENSION, source_file=new_filename)

        logger.info(f"converting running...{new_filename}")

        try:
            await exec_run(cmd, timeout=PDF_CONV_COMMAND_TIMEOUT)
        except Exception as e:
            logger.exception(e)
            return JSONResponse(
                content="에러가 발생하였습니다", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    finally:
        if new_filename:
            os.remove(new_filename)

    logger.info(f"converting complete...{saved_pdf}")

    headers = {
        "Content-Disposition": "attachment; filename*=UTF-8''{}".format(
            quote(saved_pdf.encode("utf-8"))
        )
    }

    return FileResponse(saved_pdf, media_type="application/pdf", headers=headers)


async def exec_run(cmd: str, timeout: float) -> None:
    try:
        await asyncio.wait_for(run_command(cmd), timeout=timeout)
    except asyncio.TimeoutError:
        raise RuntimeError("함수 실행이 시간 초과되었습니다")


async def run_command(cmd: str) -> None:
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(
            f"명령을 실행하는 도중에 문제가 발생하였습니다. command return code is {proc.returncode}"
        )

    if stderr:
        logger.error(stderr.decode())
