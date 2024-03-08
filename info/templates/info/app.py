from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained("PipableAI/pipSQL-1.3b", device_map="auto", offload_folder="offload")
mps_device = torch.device("mps")
model = model.to(mps_device)
tokenizer = AutoTokenizer.from_pretrained("PipableAI/pipSQL-1.3b")

app = Flask(__name__)
prompt = f"""<schema>
    CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE TABLE IF NOT EXISTS "info_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "info_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "info_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "info_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "info_attendanceclass" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "status" integer NOT NULL, "assign_id" integer NOT NULL REFERENCES "info_assign" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "info_dept" ("id" varchar(100) NOT NULL PRIMARY KEY, "name" varchar(200) NOT NULL);
CREATE TABLE IF NOT EXISTS "info_marksclass" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL, "status" bool NOT NULL, "assign_id" integer NOT NULL REFERENCES "info_assign" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "info_studentcourse" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "course_id" varchar(50) NOT NULL REFERENCES "info_course" ("id") DEFERRABLE INITIALLY DEFERRED, "student_id" varchar(100) NOT NULL REFERENCES "info_student" ("USN") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "info_marks" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL, "marks1" integer NOT NULL, "studentcourse_id" integer NOT NULL REFERENCES "info_studentcourse" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "info_user_groups_user_id_group_id_1b352364_uniq" ON "info_user_groups" ("user_id", "group_id");
CREATE INDEX "info_user_groups_user_id_583ab83a" ON "info_user_groups" ("user_id");
CREATE INDEX "info_user_groups_group_id_40dffdbb" ON "info_user_groups" ("group_id");
CREATE UNIQUE INDEX "info_user_user_permissions_user_id_permission_id_86ac821e_uniq" ON "info_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "info_user_user_permissions_user_id_ffc10b58" ON "info_user_user_permissions" ("user_id");
CREATE INDEX "info_user_user_permissions_permission_id_839364f4" ON "info_user_user_permissions" ("permission_id");
CREATE INDEX "info_attendanceclass_assign_id_8241361c" ON "info_attendanceclass" ("assign_id");
CREATE INDEX "info_marksclass_assign_id_06c0e888" ON "info_marksclass" ("assign_id");
CREATE INDEX "info_studentcourse_course_id_2aac8b3b" ON "info_studentcourse" ("course_id");
CREATE INDEX "info_studentcourse_student_id_824a5a25" ON "info_studentcourse" ("student_id");
CREATE INDEX "info_marks_studentcourse_id_9db4f113" ON "info_marks" ("studentcourse_id");
CREATE TABLE IF NOT EXISTS "info_course" ("id" varchar(50) NOT NULL PRIMARY KEY, "name" varchar(50) NOT NULL, "shortname" varchar(50) NOT NULL, "dept_id" varchar(100) NOT NULL REFERENCES "info_dept" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "info_course_dept_id_8783e216" ON "info_course" ("dept_id");
CREATE TABLE IF NOT EXISTS "info_class" ("id" varchar(100) NOT NULL PRIMARY KEY, "section" varchar(100) NOT NULL, "sem" integer NOT NULL, "dept_id" varchar(100) NOT NULL REFERENCES "info_dept" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "info_class_dept_id_eac78ba6" ON "info_class" ("dept_id");
CREATE TABLE IF NOT EXISTS "info_attendancetotal" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "course_id" varchar(50) NOT NULL REFERENCES "info_course" ("id") DEFERRABLE INITIALLY DEFERRED, "student_id" varchar(100) NOT NULL REFERENCES "info_student" ("USN") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "info_attendancetotal_course_id_d7c45376" ON "info_attendancetotal" ("course_id");
CREATE INDEX "info_attendancetotal_student_id_47e719b1" ON "info_attendancetotal" ("student_id");
CREATE TABLE IF NOT EXISTS "info_attendance" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "status" bool NOT NULL, "attendanceclass_id" integer NOT NULL REFERENCES "info_attendanceclass" ("id") DEFERRABLE INITIALLY DEFERRED, "course_id" varchar(50) NOT NULL REFERENCES "info_course" ("id") DEFERRABLE INITIALLY DEFERRED, "student_id" varchar(100) NOT NULL REFERENCES "info_student" ("USN") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "info_attendance_attendanceclass_id_165ae557" ON "info_attendance" ("attendanceclass_id");
CREATE INDEX "info_attendance_course_id_862fb2a9" ON "info_attendance" ("course_id");
CREATE INDEX "info_attendance_student_id_a3848ef5" ON "info_attendance" ("student_id");
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action_time" datetime NOT NULL, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "info_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_flag" smallint unsigned NOT NULL);
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE TABLE IF NOT EXISTS "info_student" ("USN" varchar(100) NOT NULL PRIMARY KEY, "name" varchar(200) NOT NULL, "sex" varchar(50) NOT NULL, "class_id_id" varchar(100) NOT NULL REFERENCES "info_class" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL UNIQUE REFERENCES "info_user" ("id") DEFERRABLE INITIALLY DEFERRED, "DOB" date NOT NULL);
CREATE INDEX "info_student_class_id_id_49fe47c8" ON "info_student" ("class_id_id");
CREATE UNIQUE INDEX "info_studentcourse_student_id_course_id_96c683ba_uniq" ON "info_studentcourse" ("student_id", "course_id");
CREATE TABLE IF NOT EXISTS "info_assign" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "class_id_id" varchar(100) NOT NULL REFERENCES "info_class" ("id") DEFERRABLE INITIALLY DEFERRED, "course_id" varchar(50) NOT NULL REFERENCES "info_course" ("id") DEFERRABLE INITIALLY DEFERRED, "teacher_id" varchar(100) NOT NULL REFERENCES "info_teacher" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "info_assign_class_id_id_97445caa" ON "info_assign" ("class_id_id");
CREATE INDEX "info_assign_course_id_50da791d" ON "info_assign" ("course_id");
CREATE INDEX "info_assign_teacher_id_4cc729a9" ON "info_assign" ("teacher_id");
CREATE UNIQUE INDEX "info_assign_course_id_class_id_id_teacher_id_fd958bf0_uniq" ON "info_assign" ("course_id", "class_id_id", "teacher_id");
CREATE UNIQUE INDEX "info_marks_studentcourse_id_name_1091fffa_uniq" ON "info_marks" ("studentcourse_id", "name");
CREATE UNIQUE INDEX "info_marksclass_assign_id_name_e0207692_uniq" ON "info_marksclass" ("assign_id", "name");
CREATE UNIQUE INDEX "info_attendancetotal_student_id_course_id_f5461a1c_uniq" ON "info_attendancetotal" ("student_id", "course_id");
CREATE TABLE IF NOT EXISTS "info_assigntime" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "period" varchar(50) NOT NULL, "assign_id" integer NOT NULL REFERENCES "info_assign" ("id") DEFERRABLE INITIALLY DEFERRED, "day" varchar(15) NOT NULL);
CREATE INDEX "info_assigntime_assign_id_dea972e8" ON "info_assigntime" ("assign_id");
CREATE TABLE IF NOT EXISTS "info_teacher" ("id" varchar(100) NOT NULL PRIMARY KEY, "name" varchar(100) NOT NULL, "sex" varchar(50) NOT NULL, "DOB" date NOT NULL, "user_id" integer NULL UNIQUE REFERENCES "info_user" ("id") DEFERRABLE INITIALLY DEFERRED, "dept_id" varchar(100) NOT NULL REFERENCES "info_dept" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "info_teacher_dept_id_e65acdf7" ON "info_teacher" ("dept_id");
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "info_attendancerange" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "start_date" date NOT NULL, "end_date" date NOT NULL);
CREATE TABLE IF NOT EXISTS "info_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(30) NOT NULL);
CREATE TABLE IF NOT EXISTS "authtoken_token" ("key" varchar(40) NOT NULL PRIMARY KEY, "created" datetime NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "info_user" ("id") DEFERRABLE INITIALLY DEFERRED);
  </schema>
  <question>"""
@app.route('/')
def index():
    return render_template('llmview.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json['message']
    message = "There are 3 students who are male."
    print(message)
    response = {'message': message}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
