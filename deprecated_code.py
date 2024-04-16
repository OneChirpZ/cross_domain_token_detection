# # from main.py
# def test_keyname_compare(only_hash=False, enable_verbose_print=True):
#     """
#     测试 find_tokens_by_keyname 和 find_tokens_by_compare
#     :param only_hash: 只测试 pre_process.py 预处理后的 har 文件（带 _md5.har 后缀）
#     """
#
#     har_files = os.listdir("./har_files")
#     count = 0
#     for har_file in har_files:
#         if har_file.endswith(".har"):
#             if only_hash and not har_file.endswith("_md5.har"):
#                 continue
#
#             with open(os.path.join("./har_files", har_file), "r", encoding="utf-8-sig") as f:
#                 har = json.load(f)
#
#             count += 1
#             print(f"\n{bold_split}\nFind tokens by keyname, processing {har_file}...\n")
#
#             res_keyname = find_tokens_by_keyname(har,
#                                                  enable_verbose_print=enable_verbose_print)
#
#             print(f"\n{bold_split}\nFind tokens by compare, processing {har_file}...\n")
#
#             res_compare = find_tokens_by_compare(har,
#                                                  enable_verbose_print=enable_verbose_print,
#                                                  only_multi=True)
#
#             print(f"{bold_split}")
#
#     print(f"HAR files tested: {count}\n{bold_split}")

