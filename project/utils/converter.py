#################
# DEPRECATED
#################

# import uno
# from loguru import logger
#
#
# def convert_xlsx_to_pdf(source_file, target_file) -> None:
#     try:
#         # LibreOffice 인스턴스 시작
#         local_context = uno.getComponentContext()
#         resolver = local_context.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",
#                                                                           local_context)
#         context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
#         desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
#     except Exception as e:
#         logger.exception(e)
#         raise ValueError('인스턴스를 시작하는 도중에 문제가 발생하였습니다')
#
#     document = None
#
#     try:
#         # Calc 문서 열기
#         document = desktop.loadComponentFromURL("file://" + source_file, "_blank", 0, ())
#     except Exception as e:
#         logger.exception(e)
#         raise ValueError('파일을 읽는데 실패하였습니다')
#
#     else:
#         # PDF로 변환하기 위한 속성 설정
#         export_props = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
#         export_props.Name = "FilterName"
#         export_props.Value = "writer_pdf_Export"
#
#         # 문서를 PDF로 변환하여 저장
#         document.storeToURL("file://" + target_file, (export_props,))
#
#     finally:
#         # LibreOffice 종료
#         if document:
#             document.close(True)
#
