# backend/annotation_types/scoring.py

from .base import BaseAnnotation
from database.db_utils import get_connection

class ScoringAnnotation(BaseAnnotation):
    """
    示例：1~5分的打分标注逻辑
    """
    def get_next_data(self, username: str):
        """
        获取该用户还未标注的下一条数据
        """
        conn = get_connection()
        cur = conn.cursor()
        
        # 找到用户还没标注过的记录
        # 简化逻辑：只要 annotation_result 里没有该用户的记录就算是未标注
        query = """
        SELECT d.id, d.textA, d.textB
        FROM annotation_data d
        WHERE d.id NOT IN (
            SELECT data_id FROM annotation_result WHERE username = ?
        )
        LIMIT 1
        """
        cur.execute(query, (username,))
        row = cur.fetchone()
        conn.close()

        if row:
            return {
                "id": row["id"],
                "textA": row["textA"],
                "textB": row["textB"]
            }
        else:
            # 没有更多数据了
            return None

    def submit_annotation(self, data_id: int, username: str, score: int):
        """
        提交标注结果
        """
        conn = get_connection()
        cur = conn.cursor()

        # 插入到 annotation_result
        cur.execute("""
            INSERT INTO annotation_result (data_id, username, score)
            VALUES (?, ?, ?)
        """, (data_id, username, score))

        # 如果需要的话，可以在这里将 annotation_data.is_annotated 标记为 1
        # 但要区分是否仅当所有用户都标注完才标记
        cur.execute("""
            UPDATE annotation_data
            SET is_annotated = 1
            WHERE id = ?
        """, (data_id,))

        conn.commit()
        conn.close()

    def get_progress(self, username: str):
        """
        获取用户的标注进度
        """
        conn = get_connection()
        cur = conn.cursor()

        # 总数据量
        cur.execute("SELECT COUNT(*) as total FROM annotation_data")
        total = cur.fetchone()["total"]

        # 用户已经标注的数量
        cur.execute("""
            SELECT COUNT(*) as completed
            FROM annotation_result
            WHERE username = ?
        """, (username,))
        completed = cur.fetchone()["completed"]

        conn.close()

        return {
            "completed": completed,
            "total": total
        }
