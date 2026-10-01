import pandas as pd  # CSV 파일을 읽기 위해 pandas를 불러온다.

# 이벤트 로그 CSV 파일을 읽어서 events라는 표로 저장한다.
events = pd.read_csv("event_logs.csv")

# 주문 DB 데이터를 읽는다.
orders = pd.read_csv("orders_db.csv")

# event_id 컬럼에서 중복된 값이 있는 모든 행을 찾는다.
# duplicated(keep=False)는 중복된 값에 해당하는 행을 전부 표시한다.
duplicate_event_rows = events[
    events["event_id"].duplicated(keep=False)
]

# 실제로 어떤 이벤트가 중복됐는지 결과를 확인한다.
print("event_id 중복 행:")
print(duplicate_event_rows)

# event_name이 order_created인 행에서 order_id만 가져온다.
created_order_ids = events[
    events["event_name"] == "order_created"
]["order_id"]

# payment_completed 이벤트만 가져온다.
payment_events = events[
    events["event_name"] == "payment_completed"
]

# payment_completed는 있지만,
# 같은 order_id의 order_created가 없는 행을 찾는다.
payment_without_created = payment_events[
    ~payment_events["order_id"].isin(created_order_ids)
]

# 검사 결과를 확인한다.
print("\norder_created 없이 payment_completed가 발생한 행:")
print(payment_without_created)

# DB에서 상태가 cancelled인 주문만 찾는다.
cancelled_orders = orders[
    orders["status"] == "cancelled"
]

# 취소 주문의 order_id만 가져온다.
cancelled_order_ids = cancelled_orders["order_id"]

# payment_completed 이벤트만 찾는다.
payment_events = events[
    events["event_name"] == "payment_completed"
]

# 취소된 주문인데 payment_completed 이벤트가 존재하는 행을 찾는다.
payment_for_cancelled_orders = payment_events[
    payment_events["order_id"].isin(cancelled_order_ids)
]

# 검사 결과를 확인한다.
print("\n취소 주문에 payment_completed가 존재하는 행:")
print(payment_for_cancelled_orders)

# DB에서 completed 상태인 주문만 찾는다.
completed_orders = orders[
    orders["status"] == "completed"
]

# payment_completed 이벤트만 찾는다.
payment_events = events[
    events["event_name"] == "payment_completed"
]

# payment_completed가 발생한 order_id만 가져온다.
payment_order_ids = payment_events["order_id"]

# completed 주문 중에서
# payment_completed 이벤트가 없는 주문을 찾는다.
completed_without_payment = completed_orders[
    ~completed_orders["order_id"].isin(payment_order_ids)
]

# 검사 결과를 확인한다.
print("\ncompleted인데 payment_completed가 없는 주문:")
print(completed_without_payment)

# DB에서 pending 상태인 주문만 찾는다.
pending_orders = orders[
    orders["status"] == "pending"
]

# pending 주문의 order_id만 가져온다.
pending_order_ids = pending_orders["order_id"]

# 이벤트 로그에서 pending 주문과 같은 order_id를 가진 행만 찾는다.
pending_order_events = events[
    events["order_id"].isin(pending_order_ids)
]

# DB에서는 pending인데
# 이벤트에 기록된 status가 pending이 아닌 행을 찾는다.
pending_status_mismatch = pending_order_events[
    pending_order_events["status"] != "pending"
]

# 검사 결과를 확인한다.
print("\nDB는 pending인데 Event status가 다른 행:")
print(pending_status_mismatch)

# event_id가 NULL인 행을 찾는다.
missing_event_id = events[
    events["event_id"].isna()
]

# order_id가 NULL인 행을 찾는다.
missing_order_id = events[
    events["order_id"].isna()
]

# event_name이 NULL인 행을 찾는다.
missing_event_name = events[
    events["event_name"].isna()
]

# event_time이 NULL인 행을 찾는다.
missing_event_time = events[
    events["event_time"].isna()
]

# 각 필수값의 NULL 검사 결과를 확인한다.
print("\nevent_id NULL:")
print(missing_event_id)

print("\norder_id NULL:")
print(missing_order_id)

print("\nevent_name NULL:")
print(missing_event_name)

print("\nevent_time NULL:")
print(missing_event_time)

# 이 프로젝트에서 허용하는 이벤트 이름을 정의한다.
valid_event_names = [
    "order_created",
    "payment_completed",
    "order_cancelled"
]

# 허용된 이벤트 이름에 포함되지 않는 행을 찾는다.
invalid_event_name_rows = events[
    ~events["event_name"].isin(valid_event_names)
]

# 허용값 위반 여부를 확인한다.
print("\nevent_name 허용값 위반:")
print(invalid_event_name_rows)