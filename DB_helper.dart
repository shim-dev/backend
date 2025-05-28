// // // 로컬 DB
// // import 'package:path/path.dart';
// // import 'package:sqflite/sqflite.dart';
// //
// // class DBHelper {
// //   // ✅ DB 초기화
// //   static Future<Database> initDB() async {
// //     return openDatabase(
// //       join(await getDatabasesPath(), 'meal_records.db'),
// //       onCreate: (db, version) async {
// //         // 1. 식단 기록 테이블
// //         await db.execute('''
// //     CREATE TABLE records (
// //       id INTEGER PRIMARY KEY AUTOINCREMENT,
// //       date TEXT,
// //       mealType TEXT,
// //       name TEXT,
// //       kcal REAL,
// //       water_g REAL,
// //       protein_g REAL,
// //       fat_g REAL,
// //       carbohydrate_g REAL,
// //       sugars_g REAL,
// //       fiber_g REAL,
// //       calcium_mg REAL,
// //       sodium_mg REAL,
// //       potassium_mg REAL,
// //       vitamin_a_ug_RAE REAL,
// //       retinol_ug REAL,
// //       beta_carotene_ug REAL,
// //       vitamin_c_mg REAL,
// //       vitamin_e_mg_ATE REAL,
// //       selenium_ug REAL,
// //       zinc_mg REAL,
// //       copper_ug REAL,
// //       magnesium_mg REAL,
// //       manganese_mg REAL,
// //       alpha_linolenic_acid_g REAL,
// //       epa_mg REAL,
// //       omega3_fatty_acid_g REAL,
// //       threonine_mg REAL,
// //       lysine_mg REAL,
// //       leucine_mg REAL,
// //       glutamic_acid_mg REAL,
// //       glycine_mg REAL,
// //       folate_ug_DFE REAL,
// //       saturated_fat_g REAL,
// //       trans_fat_g REAL,
// //       trans_linoleic_acid_mg REAL,
// //       trans_oleic_acid_mg REAL,
// //       trans_linolenic_acid_mg REAL,
// //       glucose_g REAL,
// //       fructose_g REAL,
// //       cholesterol_mg REAL,
// //       lauric_acid_mg REAL,
// //       myristic_acid_mg REAL,
// //       palmitic_acid_mg REAL,
// //       stearic_acid_mg REAL,
// //       behenic_acid_mg REAL
// //     )
// //   ''');
// //
// //         // 2. 물컵 기록 테이블
// //         await db.execute('''
// //         CREATE TABLE water_records (
// //           date TEXT PRIMARY KEY,
// //           cups INTEGER
// //         )
// //       ''');
// //
// //         // 3. 수면 기록 테이블
// //         await db.execute('''
// //         CREATE TABLE sleep_hours (
// //           date TEXT PRIMARY KEY,
// //           hours REAL
// //         )
// //       ''');
// //       },
// //
// //       version: 1,
// //     );
// //   }
// //
// //   // ✅ 기록 추가 (Insert)
// //   static Future<void> insertRecord(Map<String, dynamic> data) async {
// //     final db = await initDB();
// //     await db.insert(
// //       'records',
// //       data,
// //       conflictAlgorithm: ConflictAlgorithm.replace,
// //     );
// //   }
// //
// //   // ✅ 기록 불러오기 (날짜 + 식사타입)
// //   static Future<List<Map<String, dynamic>>> getRecords(
// //     String date,
// //     String mealType,
// //   ) async {
// //     final db = await initDB();
// //     return db.query(
// //       'records',
// //       where: 'date = ? AND mealType = ?',
// //       whereArgs: [date, mealType],
// //     );
// //   }
// //
// //   // ✅ 기록 삭제 (음식 하나 삭제)
// //   static Future<void> deleteRecord(int id) async {
// //     final db = await initDB();
// //     await db.delete('records', where: 'id = ?', whereArgs: [id]);
// //   }
// //
// //   static Future<void> updateRecord(int id, Map<String, dynamic> data) async {
// //     final db = await initDB();
// //     await db.update('records', data, where: 'id = ?', whereArgs: [id]);
// //   }
// //
// //   static Future<List<Map<String, dynamic>>> getRecords1(String mealType) async {
// //     final db = await initDB();
// //     DateTime today = DateTime.now();
// //     String formattedDate =
// //         '${today.year}.${today.month.toString().padLeft(2, '0')}.${today.day.toString().padLeft(2, '0')}';
// //
// //     return await db.query(
// //       'records',
// //       where: 'mealType = ? AND date = ?',
// //       whereArgs: [mealType, formattedDate],
// //     );
// //   }
// //
// //   static Future<List<Map<String, dynamic>>> getRecordsByDate(
// //     String mealType,
// //     String date,
// //   ) async {
// //     final db = await initDB();
// //     return await db.query(
// //       'records',
// //       where: 'mealType = ? AND date = ?',
// //       whereArgs: [mealType, date],
// //     );
// //   }
// //
// //   // 오늘 물컵 기록 저장
// //   static Future<void> saveWaterCups(int cups) async {
// //     final db = await initDB();
// //     print('[DEBUG] 물컵 저장 호출: $cups');
// //     await db.insert('water_records', {
// //       'date': todayStr(),
// //       'cups': cups,
// //     }, conflictAlgorithm: ConflictAlgorithm.replace);
// //   }
// //
// //   // 오늘 물컵 불러오기
// //   static Future<int> getTodayCups() async {
// //     final db = await initDB();
// //     final result = await db.query(
// //       'water_records',
// //       where: 'date = ?',
// //       whereArgs: [todayStr()],
// //     );
// //     if (result.isNotEmpty) return result.first['cups'] as int;
// //     return 0;
// //   }
// //
// //   // 오늘 날짜를 "yyyy.MM.dd" 형태로 반환
// //   static String todayStr() {
// //     final now = DateTime.now();
// //     return '${now.year}.${now.month.toString().padLeft(2, '0')}.${now.day.toString().padLeft(2, '0')}';
// //   }
// //
// //   // sleep 관련 함수 예시
// //   static Future<void> insertOrUpdateSleep(double hours, String date) async {
// //     final db = await initDB();
// //     var exist = await db.query(
// //       'sleep_hours',
// //       where: 'date = ?',
// //       whereArgs: [date],
// //     );
// //     if (exist.isNotEmpty) {
// //       await db.update(
// //         'sleep_hours',
// //         {'hours': hours},
// //         where: 'date = ?',
// //         whereArgs: [date],
// //       );
// //     } else {
// //       await db.insert('sleep_hours', {'date': date, 'hours': hours});
// //     }
// //   }
// //
// //   static Future<double> getSleep(String date) async {
// //     final db = await initDB();
// //     var data = await db.query(
// //       'sleep_hours',
// //       where: 'date = ?',
// //       whereArgs: [date],
// //     );
// //     if (data.isNotEmpty) {
// //       return (data.first['hours'] as num?)?.toDouble() ?? 0.0;
// //     }
// //     return 0.0;
// //   }
// // }
//
// //version02
// // import 'dart:convert';
// //
// // import 'package:http/http.dart' as http;
// //
// // class DBHelper {
// //   static const String apiBase = 'http://59.5.184.5:5000'; // 실제 서버 주소로 변경
// //
// //   // 오늘 날짜를 "yyyy.MM.dd" 형태로 반환
// //   static String todayStr() {
// //     final now = DateTime.now();
// //     return '${now.year}.${now.month.toString().padLeft(2, '0')}.${now.day.toString().padLeft(2, '0')}';
// //   }
// //
// //   // ✅ 기록 추가 (Insert)
// //   static Future<void> insertRecord(Map<String, dynamic> data) async {
// //     final response = await http.post(
// //       Uri.parse('$apiBase/insert_record'),
// //       headers: {'Content-Type': 'application/json'},
// //       body: jsonEncode(data),
// //     );
// //     if (response.statusCode != 200) {
// //       throw Exception('Failed to insert record');
// //     }
// //   }
// //
// //   // ✅ 기록 불러오기 (날짜 + 식사타입)
// //   static Future<List<Map<String, dynamic>>> getRecords(
// //     String date,
// //     String mealType,
// //   ) async {
// //     final response = await http.get(
// //       Uri.parse('$apiBase/get_records?date=$date&mealType=$mealType'),
// //     );
// //     if (response.statusCode == 200) {
// //       final List<dynamic> data = jsonDecode(response.body);
// //       return data.map<Map<String, dynamic>>((e) {
// //         // MongoDB의 ObjectId 변환
// //         if (e['_id'] is Map && e['_id']['\$oid'] != null) {
// //           e['_id'] = e['_id']['\$oid'];
// //         }
// //         return Map<String, dynamic>.from(e);
// //       }).toList();
// //     } else {
// //       throw Exception('Failed to get records');
// //     }
// //   }
// //
// //   // ✅ 기록 삭제 (음식 하나 삭제)
// //   static Future<void> deleteRecord(String id) async {
// //     final response = await http.delete(
// //       Uri.parse('$apiBase/delete_record?id=$id'),
// //     );
// //     if (response.statusCode != 200) {
// //       throw Exception('Failed to delete record');
// //     }
// //   }
// //
// //   // ✅ 기록 업데이트
// //   static Future<void> updateRecord(String id, Map<String, dynamic> data) async {
// //     print("[DEBUG] updateRecord 요청: id=$id, data=$data");
// //     data['_id'] = id;
// //     final response = await http.put(
// //       Uri.parse('$apiBase/update_record'),
// //       headers: {'Content-Type': 'application/json'},
// //       body: jsonEncode(data),
// //     );
// //     if (response.statusCode != 200) {
// //       throw Exception('Failed to update record');
// //     }
// //   }
// //
// //   // ✅ 오늘 날짜의 특정 식사 기록
// //   static Future<List<Map<String, dynamic>>> getRecords1(String mealType) async {
// //     String date = todayStr();
// //     return getRecords(date, mealType);
// //   }
// //
// //   // ✅ 특정 날짜의 특정 식사 기록
// //   static Future<List<Map<String, dynamic>>> getRecordsByDate(
// //     String mealType,
// //     String date,
// //   ) async {
// //     return getRecords(date, mealType);
// //   }
// //
// //   // ✅ 오늘 물컵 기록 저장
// //   static Future<void> saveWaterCups(int cups) async {
// //     final response = await http.post(
// //       Uri.parse('$apiBase/save_water'),
// //       headers: {'Content-Type': 'application/json'},
// //       body: jsonEncode({'date': todayStr(), 'cups': cups}),
// //     );
// //     if (response.statusCode != 200) {
// //       throw Exception('Failed to save water cups');
// //     }
// //   }
// //
// //   // ✅ 특정 날짜의 물컵 기록 불러오기
// //   static Future<int> getWaterCups(String date) async {
// //     final response = await http.get(Uri.parse('$apiBase/get_water?date=$date'));
// //     if (response.statusCode == 200) {
// //       final data = jsonDecode(response.body);
// //       return (data['cups'] as int?) ?? 0;
// //     }
// //     return 0;
// //   }
// //
// //   // ✅ 오늘 물컵 불러오기
// //   static Future<int> getTodayCups() async {
// //     final response = await http.get(
// //       Uri.parse('$apiBase/get_water?date=${todayStr()}'),
// //     );
// //     if (response.statusCode == 200) {
// //       final data = jsonDecode(response.body);
// //       return data['cups'] ?? 0;
// //     }
// //     return 0;
// //   }
// //
// //   // ✅ 수면 기록 저장/수정
// //   static Future<void> insertOrUpdateSleep(double hours, String date) async {
// //     final response = await http.post(
// //       Uri.parse('$apiBase/insert_or_update_sleep'),
// //       headers: {'Content-Type': 'application/json'},
// //       body: jsonEncode({'date': date, 'hours': hours}),
// //     );
// //     if (response.statusCode != 200) {
// //       throw Exception('Failed to insert/update sleep');
// //     }
// //   }
// //
// //   // ✅ 수면 기록 불러오기
// //   static Future<double> getSleep(String date) async {
// //     final response = await http.get(Uri.parse('$apiBase/get_sleep?date=$date'));
// //     if (response.statusCode == 200) {
// //       final data = jsonDecode(response.body);
// //       return (data['hours'] as num?)?.toDouble() ?? 0.0;
// //     }
// //     return 0.0;
// //   }
// //
// //   // ✅ 모든 기록 가져오기 -- 거북이 키울 때 쓰는 코드 아직 실험 중.. 왜안되는데 싯팔 진짜
// //   static Future<List<Map<String, dynamic>>> getAllRecords() async {
// //     final response = await http.get(Uri.parse('$apiBase/get_all_records'));
// //     if (response.statusCode == 200) {
// //       final List<dynamic> data = jsonDecode(response.body);
// //       return data.map<Map<String, dynamic>>((e) {
// //         // MongoDB의 ObjectId 변환
// //         if (e['_id'] is Map && e['_id']['\$oid'] != null) {
// //           e['_id'] = e['_id']['\$oid'];
// //         }
// //         return Map<String, dynamic>.from(e);
// //       }).toList();
// //     } else {
// //       throw Exception('Failed to get all records');
// //     }
// //   }
// // }

import 'dart:convert';
import 'dart:io';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

class DBHelper {
  static const String apiBase = 'http://125.128.179.118:5000';
  static final FlutterSecureStorage _storage = FlutterSecureStorage();

  static String todayStr() {
    final now = DateTime.now();
    return '${now.year}.${now.month.toString().padLeft(2, '0')}.${now.day.toString().padLeft(2, '0')}';
  }

  // userId 읽는 함수 (필수)
  static Future<String> _getUserId() async {
    String? userId = await _storage.read(key: 'user_id');
    if (userId == null) throw Exception('로그인 정보 없음!');
    return userId;
  }

  // ✅ 기록 추가 (Insert)
  static Future<void> insertRecord(Map<String, dynamic> data) async {
    final userId = await _getUserId();
    print('[DEBUG] insertRecord - user_id: $userId');
    final mergedData = {...data, 'user_id': userId};
    final response = await http.post(
      Uri.parse('$apiBase/insert_record'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(mergedData),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to insert record');
    }
  }

  // ✅ 기록 불러오기 (날짜 + 식사타입)
  static Future<List<Map<String, dynamic>>> getRecords(
    String date,
    String mealType,
  ) async {
    final userId = await _getUserId();
    final response = await http.get(
      Uri.parse(
        '$apiBase/get_records?user_id=$userId&date=$date&mealType=$mealType',
      ),
    );
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map<Map<String, dynamic>>((e) {
        if (e['_id'] is Map && e['_id']['\$oid'] != null) {
          e['_id'] = e['_id']['\$oid'];
        }
        return Map<String, dynamic>.from(e);
      }).toList();
    } else {
      throw Exception('Failed to get records');
    }
  }

  // ✅ 기록 삭제
  static Future<void> deleteRecord(String id) async {
    final userId = await _getUserId();
    final response = await http.delete(
      Uri.parse('$apiBase/delete_record?id=$id&user_id=$userId'),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to delete record');
    }
  }

  // ✅ 기록 업데이트
  static Future<void> updateRecord(String id, Map<String, dynamic> data) async {
    final userId = await _getUserId();
    data['_id'] = id;
    data['user_id'] = userId;
    final response = await http.put(
      Uri.parse('$apiBase/update_record'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(data),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to update record');
    }
  }

  // ✅ 오늘 날짜의 특정 식사 기록
  static Future<List<Map<String, dynamic>>> getRecords1(String mealType) async {
    String date = todayStr();
    return getRecords(date, mealType);
  }

  // ✅ 특정 날짜의 특정 식사 기록
  static Future<List<Map<String, dynamic>>> getRecordsByDate(
    String mealType,
    String date,
  ) async {
    return getRecords(date, mealType);
  }

  // ✅ 오늘 물컵 기록 저장
  static Future<void> saveWaterCups(int cups) async {
    final userId = await _getUserId();
    final response = await http.post(
      Uri.parse('$apiBase/save_water'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'user_id': userId, 'date': todayStr(), 'cups': cups}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to save water cups');
    }
  }

  // ✅ 특정 날짜의 물컵 기록 불러오기
  static Future<int> getWaterCups(String date) async {
    final userId = await _getUserId();
    final response = await http.get(
      Uri.parse('$apiBase/get_water?user_id=$userId&date=$date'),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return (data['cups'] as int?) ?? 0;
    }
    return 0;
  }

  // ✅ 오늘 물컵 불러오기
  static Future<int> getTodayCups() async {
    final userId = await _getUserId();
    final response = await http.get(
      Uri.parse('$apiBase/get_water?user_id=$userId&date=${todayStr()}'),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['cups'] ?? 0;
    }
    return 0;
  }

  // ✅ 수면 기록 저장/수정
  static Future<void> insertOrUpdateSleep(double hours, String date) async {
    final userId = await _getUserId();
    final response = await http.post(
      Uri.parse('$apiBase/insert_or_update_sleep'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'user_id': userId, 'date': date, 'hours': hours}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to insert/update sleep');
    }
  }

  // ✅ 수면 기록 불러오기
  static Future<double> getSleep(String date) async {
    final userId = await _getUserId();
    final response = await http.get(
      Uri.parse('$apiBase/get_sleep?user_id=$userId&date=$date'),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return (data['hours'] as num?)?.toDouble() ?? 0.0;
    }
    return 0.0;
  }

  // ✅ 모든 기록 가져오기 (유저별)
  static Future<List<Map<String, dynamic>>> getAllRecords() async {
    final userId = await _getUserId();
    final response = await http.get(
      Uri.parse('$apiBase/get_all_records?user_id=$userId'),
    );
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map<Map<String, dynamic>>((e) {
        if (e['_id'] is Map && e['_id']['\$oid'] != null) {
          e['_id'] = e['_id']['\$oid'];
        }
        return Map<String, dynamic>.from(e);
      }).toList();
    } else {
      throw Exception('Failed to get all records');
    }
  }

  // ✅ 유저 회원 가입 (유저별)
  static Future<void> signup({
    required String email,
    required String nickname,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$apiBase/signup'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'nickname': nickname,
        'password': password,
      }),
    );
    print('[DEBUG] 서버 응답: ${response.body}');
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final userId = data['user_id'];
      final nickName = data['nickname']; // 닉네임 파싱
      final email = data['email'];
      print('[DEBUG] 받은 user_id: $userId, nickname: $nickName');
      if (userId != null && userId.toString().isNotEmpty) {
        await _storage.write(key: 'user_id', value: userId);
        await _storage.write(key: 'nickname', value: nickName);
        await _storage.write(key: 'email', value: email);
        print('[DEBUG] user_id 저장 완료!');
      } else {
        throw Exception('서버에서 user_id를 못 받았어요!');
      }
    } else {
      throw Exception('회원가입 실패: ${response.body}');
    }
  }

  // ✅ 유저 로그인 (유저별)
  static Future<void> login({
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$apiBase/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    print('[DEBUG] 로그인 응답: ${response.body}');
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final userId = data['user_id'];
      final nickName = data['nickname'];
      final email = data['email'];
      if (userId != null && userId.toString().isNotEmpty) {
        await _storage.write(key: 'user_id', value: userId);
        await _storage.write(key: 'nickname', value: nickName);
        await _storage.write(key: 'email', value: email);
        print('[DEBUG] 로그인 user_id 저장 완료!');
      } else {
        throw Exception('서버에서 user_id를 못 받았어요!');
      }
    } else {
      // 서버에서 보낸 에러 메시지를 그대로 보여줄 수 있음
      String errMsg = '로그인 실패: ${response.body}';
      try {
        final data = jsonDecode(response.body);
        errMsg = data['error'] ?? errMsg;
      } catch (_) {}
      throw Exception(errMsg);
    }
  }

  // ✅ 유저 닉네임 불러오기 (유저별)
  static Future<String?> fetchNicknameFromDB() async {
    final userId = await _storage.read(key: 'user_id');
    if (userId == null) throw Exception('로그인 정보 없음');
    final response = await http.get(
      Uri.parse('$apiBase/get_nickname?user_id=$userId'),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['nickname'] as String?;
    } else {
      throw Exception('닉네임 조회 실패: ${response.body}');
    }
  }

  // ✅ 유저 닉네임 수정하기 (유저별)
  static Future<void> updateNickname(String newNickname) async {
    final userId = await _storage.read(key: 'user_id');
    if (userId == null) throw Exception('로그인 정보 없음');
    final response = await http.post(
      Uri.parse('$apiBase/update_nickname'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'user_id': userId, 'nickname': newNickname}),
    );
    if (response.statusCode == 200) {
      // storage의 nickname도 최신으로 갱신!
      await _storage.write(key: 'nickname', value: newNickname);
    } else {
      throw Exception('닉네임 변경 실패: ${response.body}');
    }
  }

  // 공지사항 정보 가지고 오기
  static Future<List<Map<String, dynamic>>> getNotices() async {
    final response = await http.get(Uri.parse('$apiBase/get_notices'));
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data
          .map<Map<String, dynamic>>((e) => Map<String, dynamic>.from(e))
          .toList();
    } else {
      throw Exception('Failed to get notices');
    }
  }

  // 이벤트 정보 가지고 오기
  static Future<List<Map<String, dynamic>>> getEvents() async {
    final response = await http.get(Uri.parse('$apiBase/get_events'));
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data
          .map<Map<String, dynamic>>((e) => Map<String, dynamic>.from(e))
          .toList();
    } else {
      throw Exception('Failed to load events');
    }
  }

  // 문의 내역 전송 이미지 버전 2

  static Future<void> insertInquiry({
    required String title,
    required String content,
    List<String>? imageIds, // 추가!
  }) async {
    final userId = await _getUserId();
    final date = todayStr();
    final body = {
      'user_id': userId,
      'title': title,
      'content': content,
      'date': date,
      'image_ids': imageIds ?? [],
    };
    final response = await http.post(
      Uri.parse('$apiBase/insert_inquiry'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(body),
    );
    if (response.statusCode != 200) {
      throw Exception('문의 저장 실패: ${response.body}');
    }
  }

  // 문의 사진을 보내는 코드..?

  static Future<String?> uploadInquiryImage(File imageFile) async {
    final userId = await _getUserId();
    final uri = Uri.parse('$apiBase/upload_image');
    final request =
        http.MultipartRequest('POST', uri)
          ..fields['user_id'] = userId
          ..files.add(
            await http.MultipartFile.fromPath('image', imageFile.path),
          );
    final response = await request.send();
    if (response.statusCode == 200) {
      final respStr = await response.stream.bytesToString();
      final respJson = jsonDecode(respStr);
      return respJson['image_id'];
    } else {
      throw Exception('이미지 업로드 실패: ${response.statusCode}');
    }
  }

  // 문의 내역 받아오기
  static Future<List<Map<String, dynamic>>> getInquiries() async {
    String? userId = await _storage.read(key: 'user_id');
    if (userId == null) throw Exception('로그인 정보 없음');
    final response = await http.get(
      Uri.parse('$apiBase/get_inquiries?user_id=$userId'),
    );
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data
          .map<Map<String, dynamic>>((e) => Map<String, dynamic>.from(e))
          .toList();
    } else {
      throw Exception('Failed to get inquiries: ${response.body}');
    }
  }

  // 회원탈퇴 사유 저장
  static Future<void> insertCancelReason({required String reason}) async {
    final userId = await _getUserId();
    final date = todayStr();
    final response = await http.post(
      Uri.parse('$apiBase/insert_cancel_reason'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'user_id': userId, 'reason': reason, 'date': date}),
    );
    if (response.statusCode != 200) {
      throw Exception('탈퇴 사유 저장 실패: ${response.body}');
    }
  }

  // 비밀 번호 변경
  static Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    final userId = await _storage.read(key: 'user_id');
    if (userId == null) throw Exception('로그인 정보 없음');

    final response = await http.post(
      Uri.parse('$apiBase/change_password'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': userId,
        'current_password': currentPassword,
        'new_password': newPassword,
      }),
    );

    if (response.statusCode == 200) {
      // 성공
      return;
    } else {
      // 실패 메시지 전달
      String errMsg = '비밀번호 변경 실패';
      try {
        final data = jsonDecode(response.body);
        errMsg = data['error'] ?? errMsg;
      } catch (_) {}
      throw Exception(errMsg);
    }
  }

  // 키워드들(해쉬태그) 들을 직접 가져오기
  static Future<List<String>> getKeywords() async {
    final response = await http.get(Uri.parse('$apiBase/get_keywords'));
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.cast<String>();
    } else {
      throw Exception('Failed to get keywords');
    }
  }

  // 실험실 DB상 레시피 불러오기!
  static Future<List<Map<String, dynamic>>> searchRecipes(
    String query, {
    String order = 'latest',
  }) async {
    final response = await http.get(
      Uri.parse('$apiBase/search_recipes?query=$query&order=$order'),
    );
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.cast<Map<String, dynamic>>();
    } else {
      throw Exception('Failed to search recipes');
    }
  }

  // 레시피 조회수 증가
  static Future<void> increaseRecipeView(String recipeId) async {
    final response = await http.post(
      Uri.parse('$apiBase/increase_recipe_view'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'id': recipeId}),
    );
    if (response.statusCode != 200) {
      print('조회수 증가 실패: ${response.body}');
    }
  }
}
