from config import TestConfig as config
import os
import pickle
import shutil
import datetime

from config.TestConfig import desktop_app_title


def get_pytest_run_command(args, run_mode_type, run_app_type, script_folder):
    """
    pytest command generator for running the execution
    :param args: command line arguments received from run test
    :param run_mode_type: can be set to bdd or scripting
    :param run_app_type: can be set to web or api
    :param script_folder: can be set to file_bdd, file_scripts, file_api
    :return: returns the pytest command
    """
    pytest_command = ["--disable-warnings", "--tb=short", "-p", "no:faulthandler"]
    report_flag = ""
    parallel_flag = ""
    last_failed_flag = ""
    rerun_flag = ""
    test_file_flag = ""
    tag_execute_flag = ""
    max_fail_flag = ""
    pytest_add_command = ""
    run_config = {}
    allure_result_path = ""
    html_report_path = ""
    allure_report_path = ""

    if run_app_type == "Web" or run_app_type == "web":
        run_config['browser'] = args.browser if args.browser else config.browser
        if run_mode_type == "scripting":
            run_config['web_url'] = args.web_url if args.web_url else config.web_url
        elif run_mode_type == "bdd":
            run_config['bdd_url'] = args.bdd_url if args.bdd_url else config.bdd_url

    if run_app_type == "api":
        run_config['rest_url'] = args.rest_url if args.rest_url else config.rest_url
        run_config['wsdl_url'] = args.wsdl_url if args.wsdl_url else config.wsdl_url

    if run_app_type == "db":
        run_config['db_uri'] = args.db_uri if args.db_uri else config.db_uri

    if run_app_type == "desktop":
        run_config['desktop_app_path'] = args.desktop_app_path if args.desktop_app_path else config.desktop_app_path
        run_config['desktop_app_title'] = args.desktop_app_title if args.desktop_app_title else config.desktop_app_title
        run_config['winapp_driver_url'] = args.winapp_driver_url if args.winapp_driver_url else config.winapp_driver_url
        run_config['winapp_driver_cap'] = args.winapp_driver_cap if args.winapp_driver_cap else config.winapp_driver_cap

    if run_app_type == "Mobile" or run_app_type == "mobile":
        # run_config['browser_mobile'] = args.browser_mobile if args.browser else config.browser_mobile
        run_config['mob_udid'] = args.mob_udid if args.mob_udid else config.mob_udid
        run_config['mob_platform'] = args.mob_platform if args.mob_platform else config.mob_platform
        run_config['mob_remote_url'] = args.mob_remote_url if args.mob_remote_url else config.mob_remote_url

    run_config['exec_type'] = 'ci' if args.docker or args.jenkins else 'local'
    run_config_file = os.path.abspath('../../resources/run_time_config.pkl')
    run_config['parallel'] = True if args.parallel or config.parallel else False


    if config.Allure_History:
        allure_result_path = os.path.abspath('../../reports/allure_reports/results')
        allure_report_path = os.path.abspath('../../reports/allure_reports/reports')
        failure_analysis_path = os.path.abspath('../../reports/allure_reports/failure-analysis')
        html_report_path = os.path.abspath('../../reports/html/')
        if os.path.exists(allure_report_path + "/history"):
            shutil.rmtree(allure_result_path + "/history", ignore_errors=True)
            shutil.move(allure_report_path + "/history", allure_result_path)
    else:
        absReport = os.path.abspath('../../reports/report_dates/')
        mydir = os.path.join(absReport, datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S'))
        if not os.path.exists(mydir):
            os.makedirs(mydir)
            allure_result_path = mydir + "/allure-results"
            allure_report_path = mydir + "/allure-reports"
            failure_analysis_path = mydir + "/failure-analysis"
            html_report_path = mydir + "/html"
            print(mydir)
            if config.ReportType == "allure":
                os.makedirs(allure_report_path)
                os.makedirs(allure_result_path)
                os.makedirs(failure_analysis_path)
            elif config.ReportType == "html":
                os.makedirs(html_report_path)
                os.makedirs(failure_analysis_path)
            else:
                os.makedirs(allure_report_path)
                os.makedirs(allure_result_path)
                os.makedirs(html_report_path)
                os.makedirs(failure_analysis_path)

    if args.jenkins:
        allure_result_path = os.path.abspath("../../reports/jenkins_results/")
        failure_analysis_path = os.path.abspath('../../reports/allure_reports/failure-analysis')

    run_config['failure_analysis'] = failure_analysis_path

    if run_mode_type == "bdd":
        run_config['bdd'] = True
        if config.ReportType == "allure":
            pytest_command.extend(["--alluredir=" + allure_result_path, "-p", "no:allure_pytest"])
            # report_flag_1 = "--alluredir=" + allure_result_path
            # report_flag_2 = " -p no:allure_pytest "
        elif config.ReportType == "html":
            pytest_command.extend(["-p", "no:allure_pytest", "--html=" + html_report_path + "/report.html", "--self-contained-html"])
            # report_flag = " -p no:allure_pytest " + "--html=" + html_report_path + "/report.html --self-contained-html"
        elif config.ReportType == "both":
            pytest_command.extend(
                ["-p", "no:allure_pytest", "--alluredir=" + allure_result_path, "--html=" + html_report_path + "/report.html", "--self-contained-html"])
            # report_flag = " -p no:allure_pytest " + "--alluredir=" + allure_result_path + " --html=" + html_report_path + "/report.html --self-contained-html"
    else:
        run_config['bdd'] = False
        if config.ReportType == "allure":
            pytest_command.extend(["--alluredir=" + allure_result_path, "-p", "no:allure_pytest_bdd"])
            # report_flag_1 = "--alluredir=" + allure_result_path
            # report_flag_2 = " -p no:allure_pytest_bdd"
        elif config.ReportType == "html":
            pytest_command.extend(
                ["-p", "no:allure_pytest_bdd", "--html=" + html_report_path + "/report.html", "--self-contained-html"])
            # report_flag = " -p no:allure_pytest_bdd " + "--html=" + html_report_path + "/report.html --self-contained-html"
        elif config.ReportType == "both":
            pytest_command.extend(
                ["-p", "no:allure_pytest_bdd", "--alluredir=" + allure_result_path,
                 "--html=" + html_report_path + "/report.html", "--self-contained-html"])
            # report_flag = " -p no:allure_pytest_bdd " + "--alluredir=" + allure_result_path + " --html=" + html_report_path + "/report.html --self-contained-html"

    if args.parallel:
        # parallel_flag = " -n " + str(args.parallel)
        pytest_command.extend(["-n", str(args.parallel)])
    elif config.parallel:
        # parallel_flag = " -n " + str(config.thread_num)
        pytest_command.extend(["-n", str(config.thread_num)])

    if args.last_failed_tests:
        pytest_command.append("--last-failed")
        # last_failed_flag = " --last-failed "
    elif config.last_failed_tests:
        pytest_command.append("--last-failed")

    if args.rerun_flaky_tests:
        pytest_command.extend(["--reruns",str(args.rerun_flaky_tests)])
        # rerun_flag = " --reruns " + str(args.rerun_flaky_tests) + " "
    elif config.rerun_flaky_tests:
        pytest_command.extend(["--reruns", str(config.rerun_flaky_tests)])
        # rerun_flag = " --reruns " + str(config.rerun_flaky_tests) + " "

    if args.test_scripts:
        pytest_command.extend(args.test_scripts)
        # test_files = " ".join(args.test_scripts)
        # test_file_flag = test_files
    elif script_folder == "file_bdd":
        if config.test_file_bdd:
            pytest_command.extend(config.test_file_bdd)
            # test_files = " ".join(config.test_file_bdd)
            # test_file_flag = test_files
    elif script_folder == "file_scripts":
        if config.test_file_scripts:
            pytest_command.extend(config.test_file_scripts)
            # test_files = " ".join(config.test_file_scripts)
            # test_file_flag = test_files
    elif script_folder == "file_e2e":
        if config.test_file_e2e:
            pytest_command.extend(config.test_file_e2e)
            # test_files = " ".join(config.test_file_e2e)
            # test_file_flag = test_files
    elif script_folder == "file_api":
        if config.test_file_api:
            pytest_command.extend(config.test_file_api)
            # test_files = " ".join(config.test_file_api)
            # test_file_flag = test_files
    elif script_folder == "file_db":
        if config.test_file_db:
            pytest_command.extend(config.test_file_db)
            # test_files = " ".join(config.test_file_db)
            # test_file_flag = test_files
    elif script_folder == "file_mobile_auto":
        if config.test_file_mobile:
            pytest_command.extend(config.test_file_mobile)
            # test_files = " ".join(config.test_file_mobile)
            # test_file_flag = test_files

    if args.tags:
        pytest_command.extend(["-m", ' or '.join(args.tags)])
        # tags = ' or '.join(args.tags)
        # tag_execute_flag = " -m \"" + tags + "\" "
    elif config.tags:
        pytest_command.extend(["-m", ' or '.join(config.tags)])
        # tags = ' or '.join(config.tags)
        # tag_execute_flag = " -m \"" + tags + "\" "

    if args.max_fail:
        pytest_command.append("--maxfail="+str(args.max_fail))
        # max_fail_flag = " --maxfail=" + str(args.max_fail) + " "
    elif config.max_fail:
        pytest_command.append("--maxfail=" + str(config.max_fail))
        # max_fail_flag = " --maxfail=" + str(config.max_fail) + " "

    if args.command_pytest:
        pytest_command.extend(args.command_pytest)
        # pytest_add_command = " " + str(args.command_pytest) + " "

    # pytest_command = [pytest_command_w,pytest_command_t, report_flag_2, report_flag_1, parallel_flag , max_fail_flag,  last_failed_flag , pytest_add_command, rerun_flag,
    #     tag_execute_flag, test_file_flag]
    pytest_command = list(filter(lambda a: a!="", pytest_command))
    
    with open(run_config_file, 'wb') as file:
        # A new file will be created
        pickle.dump(run_config, file)

    return (pytest_command, allure_result_path, allure_report_path, html_report_path, failure_analysis_path)

def get_pytest_run_command_e2e(args, run_mode_type, run_app_type, script_folder):
    """
    pytest command generator for running the execution for e2e tests
    :param args: command line arguments received from run test
    :param run_mode_type: can be set to bdd or scripting
    :param run_app_type: can be set to web or api
    :param script_folder: can be set to file_bdd, file_scripts, file_api
    :return: returns the pytest command
    """
    pytest_command = ["--disable-warnings", "--tb=short", "-p", "no:faulthandler"]
    report_flag = ""
    parallel_flag = ""
    last_failed_flag = ""
    rerun_flag = ""
    test_file_flag = ""
    tag_execute_flag = ""
    max_fail_flag = ""
    pytest_add_command = ""
    run_config = {}
    allure_result_path = ""
    html_report_path = ""
    allure_report_path = ""

    if run_app_type == "e2e":
        run_config['browser'] = args.browser if args.browser else config.browser
        run_config['web_url'] = args.web_url if args.web_url else config.web_url
        run_config['bdd_url'] = args.bdd_url if args.bdd_url else config.bdd_url
        run_config['rest_url'] = args.rest_url if args.rest_url else config.rest_url
        run_config['wsdl_url'] = args.wsdl_url if args.wsdl_url else config.wsdl_url
        run_config['db_uri'] = args.db_uri if args.db_uri else config.db_uri
        run_config['desktop_app_path'] = args.desktop_app_path if args.desktop_app_path else config.desktop_app_path
        run_config['desktop_app_title'] = args.desktop_app_title if args.desktop_app_title else config.desktop_app_title
        run_config['winapp_driver_url'] = args.winapp_driver_url if args.winapp_driver_url else config.winapp_driver_url
        run_config['winapp_driver_cap'] = args.winapp_driver_cap if args.winapp_driver_cap else config.winapp_driver_cap
        run_config['mob_udid'] = args.mob_udid if args.mob_udid else config.mob_udid
        run_config['mob_platform'] = args.mob_platform if args.mob_platform else config.mob_platform
        run_config['mob_remote_url'] = args.mob_remote_url if args.mob_remote_url else config.mob_remote_url

    run_config['exec_type'] = 'ci' if args.docker or args.jenkins else 'local'
    run_config_file = os.path.abspath('../../resources/run_time_config_e2e.pkl')

    

    if config.Allure_History:
        allure_result_path = os.path.abspath('../../reports/allure_reports/results')
        allure_report_path = os.path.abspath('../../reports/allure_reports/reports')
        failure_analysis_path = os.path.abspath('../../reports/allure_reports/failure-analysis')
        html_report_path = os.path.abspath('../../reports/html/')
        if os.path.exists(allure_report_path + "/history"):
            shutil.rmtree(allure_result_path + "/history", ignore_errors=True)
            shutil.move(allure_report_path + "/history", allure_result_path)
    else:
        absReport = os.path.abspath('../../reports/report_dates/')
        mydir = os.path.join(absReport, datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S'))
        if not os.path.exists(mydir):
            os.makedirs(mydir)
            allure_result_path = mydir + "/allure-results"
            allure_report_path = mydir + "/allure-reports"
            failure_analysis_path = mydir + "/failure-analysis"
            html_report_path = mydir + "/html"
            print(mydir)
            if config.ReportType == "allure":
                os.makedirs(allure_report_path)
                os.makedirs(allure_result_path)
                os.makedirs(failure_analysis_path)
            elif config.ReportType == "html":
                os.makedirs(html_report_path)
                os.makedirs(failure_analysis_path)
            else:
                os.makedirs(allure_report_path)
                os.makedirs(allure_result_path)
                os.makedirs(html_report_path)
                os.makedirs(failure_analysis_path)

    if args.jenkins:
        allure_result_path = os.path.abspath("../../reports/jenkins_results/")
        failure_analysis_path = os.path.abspath('../../reports/allure_reports/failure-analysis')

    run_config['failure_analysis'] = failure_analysis_path

    if run_mode_type == "bdd":
        run_config['bdd'] = True
        if config.ReportType == "allure":
            pytest_command.extend(["--alluredir=" + allure_result_path, "-p", "no:allure_pytest"])
        elif config.ReportType == "html":
            pytest_command.extend(["-p", "no:allure_pytest", "--html=" + html_report_path + "/report.html", "--self-contained-html"])
        elif config.ReportType == "both":
            pytest_command.extend(
                ["-p", "no:allure_pytest", "--alluredir=" + allure_result_path,
                 "--html=" + html_report_path + "/report.html", "--self-contained-html"])
    else:
        run_config['bdd'] = False
        if config.ReportType == "allure":
            pytest_command.extend(["--alluredir=" + allure_result_path, "-p", "no:allure_pytest_bdd"])
        elif config.ReportType == "html":
            pytest_command.extend(
                ["-p", "no:allure_pytest_bdd", "--html=" + html_report_path + "/report.html", "--self-contained-html"])
        elif config.ReportType == "both":
            pytest_command.extend(
                ["-p", "no:allure_pytest_bdd", "--alluredir=" + allure_result_path,
                 "--html=" + html_report_path + "/report.html", "--self-contained-html"])

    if args.parallel:
        pytest_command.extend(["-n", str(args.parallel)])
    elif config.parallel:
        pytest_command.extend(["-n", str(config.thread_num)])

    if args.last_failed_tests:
        pytest_command.append("--last-failed")
    elif config.last_failed_tests:
        pytest_command.append("--last-failed")

    if args.rerun_flaky_tests:
        pytest_command.extend(["--reruns", str(args.rerun_flaky_tests)])
    elif config.rerun_flaky_tests:
        pytest_command.extend(["--reruns", str(config.rerun_flaky_tests)])

    if args.test_scripts:
        pytest_command.extend(args.test_scripts)
    elif script_folder == "file_bdd":
        if config.test_file_bdd:
            pytest_command.extend(config.test_file_bdd)
    elif script_folder == "file_scripts":
        if config.test_file_scripts:
            pytest_command.extend(config.test_file_scripts)
    elif script_folder == "file_e2e":
        if config.test_file_e2e:
            pytest_command.extend(config.test_file_e2e)
    elif script_folder == "file_api":
        if config.test_file_api:
            pytest_command.extend(config.test_file_api)
    elif script_folder == "file_db":
        if config.test_file_db:
            pytest_command.extend(config.test_file_db)
    elif script_folder == "file_mobile_auto":
        if config.test_file_mobile:
            pytest_command.extend(config.test_file_mobile)

    if args.tags:
        pytest_command.extend(["-m", ' or '.join(args.tags)])
    elif config.tags:
        pytest_command.extend(["-m", ' or '.join(config.tags)])

    if args.max_fail:
        pytest_command.append("--maxfail="+str(args.max_fail))
    elif config.max_fail:
        pytest_command.append("--maxfail=" + str(config.max_fail))

    if args.command_pytest:
        pytest_command.extend(args.command_pytest)
        
    with open(run_config_file, 'wb') as file:
        # A new file will be created
        pickle.dump(run_config, file)

    return (pytest_command, allure_result_path, allure_report_path, html_report_path, failure_analysis_path)



