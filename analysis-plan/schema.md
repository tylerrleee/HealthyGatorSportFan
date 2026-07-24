Here is the complete relational data schema extracted from the provided diagram, including all tables, columns, data types, key constraints, and entity relationships.

---

## **1. Tables & Columns**

### **`user`**

* **`user_id`**: `INT` (Primary Key)


* **`email`**: `VARCHAR(254)`

* **`first_name`**: `VARCHAR(100)`

* **`last_name`**: `VARCHAR(100)`

* **`birthdate`**: `DATE`

* **`gender`**: `VARCHAR(10)`

* **`password`**: `VARCHAR(128)`

* **`push_token`**: `VARCHAR(128)`

* **`is_enrolled`**: `BOOLEAN`

* **`enrolled_at`**: `DATETIME`


---

### **`wearable_device`**

* **`id`**: `INT` (Primary Key)


* **`user_id`**: `INT` (Foreign Key $\rightarrow$ `user.user_id`)


* **`labfront_participant_id`**: `VARCHAR(64)`

* **`is_active`**: `BOOLEAN`

* **`last_synced_at`**: `DATETIME`


---

### **`heart_rate_sample`**

* **`id`**: `INT` (Primary Key)


* **`user_id`**: `INT` (Foreign Key $\rightarrow$ `user.user_id`)


* **`timestamp`**: `DATETIME`

* **`bpm`**: `SMALLINT`

* **`source`**: `VARCHAR(32)`


---

### **`stress_sample`**

* **`id`**: `INT` (Primary Key)


* **`user_id`**: `INT` (Foreign Key $\rightarrow$ `user.user_id`)


* **`timestamp`**: `DATETIME`

* **`stress_score`**: `SMALLINT`

* **`source`**: `VARCHAR(32)`


---

### **`ema`**

* **`id`**: `INT` (Primary Key)


* **`user_id`**: `INT` (Foreign Key $\rightarrow$ `user.user_id`)


* **`prompt_id`**: `VARCHAR(64)`

* **`sent_at`**: `DATETIME`

* **`responded_at`**: `DATETIME`

* **`status`**: `VARCHAR(16)`

* **`mood`**: `SMALLINT`

* **`stress`**: `SMALLINT`

* **`energy`**: `SMALLINT`


---

### **`jitai_log`**

* **`id`**: `INT` (Primary Key)


* **`user_id`**: `INT` (Foreign Key $\rightarrow$ `user.user_id`)


* **`prompt_id`**: `VARCHAR(64)`

* **`triggered_at`**: `DATETIME`

* **`trigger_reason`**: `VARCHAR(128)`

* **`hr_at_trigger`**: `SMALLINT`

* **`stress_at_trigger`**: `SMALLINT`

* **`ema_id`**: `INT` (Foreign Key $\rightarrow$ `ema.id`)


* **`observed_mssd`**: `FLOAT`

* **`send_prompt`**: `BOOLEAN`

* **`status`**: `VARCHAR(16)`

* **`decision_point_id`**: `VARCHAR(64)`

* **`randomization_probability`**: `FLOAT`

* **`randomization_draw`**: `FLOAT`

* **`trigger_signal`**: `VARCHAR(32)`

* **`ema_mood`**: `SMALLINT`

* **`ema_stress`**: `SMALLINT`

* **`ema_energy`**: `SMALLINT`

* **`eligible_prompt_ids`**: `JSONB`

* **`decision_made_at`**: `DATETIME`

* **`delivery_error`**: `TEXT`

* **`delivery_status`**: `VARCHAR(32)`

* **`device_received_at`**: `DATETIME`

* **`push_sent_at`**: `DATETIME`

* **`receipt_app_state`**: `VARCHAR(32)`

* **`receipt_platform`**: `VARCHAR(16)`

* **`receipt_reported_at`**: `DATETIME`


---

### **`phone_telemetry`**

* **`id`**: `INT` (Primary Key)


* **`user_id`**: `INT` (Foreign Key $\rightarrow$ `user.user_id`)


* **`session_id`**: `VARCHAR(64)`

* **`event_type`**: `VARCHAR(64)`

* **`occurred_at`**: `DATETIME`

* **`recorded_at`**: `DATETIME`

* **`screen_name`**: `VARCHAR(64)`

* **`latency_ms`**: `INT`

* **`metadata`**: `JSONB`


---

### **`engagement_log`**

* **`id`**: `INT` (Primary Key)


* **`user_id`**: `INT` (Foreign Key $\rightarrow$ `user.user_id`)


* **`jitai_log_id`**: `INT` (Foreign Key $\rightarrow$ `jitai_log.id`)


* **`event_type`**: `VARCHAR(64)`

* **`occurred_at`**: `DATETIME`

* **`recorded_at`**: `DATETIME`


---

## **2. Entity Relationships (Foreign Keys)**

1. **`wearable_device.user_id` $\rightarrow$ `user.user_id**` *(One-to-One / One-to-Many)*

2. **`heart_rate_sample.user_id` $\rightarrow$ `user.user_id**` *(Many-to-One)*

3. **`stress_sample.user_id` $\rightarrow$ `user.user_id**` *(Many-to-One)*

4. **`ema.user_id` $\rightarrow$ `user.user_id**` *(Many-to-One)*

5. **`jitai_log.user_id` $\rightarrow$ `user.user_id**` *(Many-to-One)*

6. **`jitai_log.ema_id` $\rightarrow$ `ema.id**` *(Many-to-One)*

7. **`phone_telemetry.user_id` $\rightarrow$ `user.user_id**` *(Many-to-One)*

8. **`engagement_log.user_id` $\rightarrow$ `user.user_id**` *(Many-to-One)*

9. **`engagement_log.jitai_log_id` $\rightarrow$ `jitai_log.id**` *(Many-to-One)*