"""
File storage utilities for MinIO integration
"""
import os
import uuid
from typing import Optional, BinaryIO
from io import BytesIO
from datetime import timedelta
from minio import Minio
from minio.error import S3Error
from app.core.config import settings


class FileStorageService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_SSL
        )
        self.resume_bucket = "resumes"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure resume bucket exists"""
        try:
            if not self.client.bucket_exists(self.resume_bucket):
                self.client.make_bucket(self.resume_bucket)
                print(f"Created bucket: {self.resume_bucket}")
        except S3Error as e:
            print(f"Error ensuring bucket exists: {e}")

    def upload_file(self, file_data: bytes, filename: str, content_type: str = "application/octet-stream") -> str:
        """
        Upload file to MinIO
        
        Args:
            file_data: File data as binary stream
            filename: Original filename
            content_type: MIME type of the file
            
        Returns:
            str: Generated filename in storage
        """
        try:
            # Generate unique filename
            file_extension = os.path.splitext(filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            
            # Upload file
            file_stream = BytesIO(file_data)
            self.client.put_object(
                bucket_name=self.resume_bucket,
                object_name=unique_filename,
                data=file_stream,
                length=len(file_data),
                content_type=content_type
            )
            
            return unique_filename
            
        except S3Error as e:
            raise Exception(f"Failed to upload file to MinIO: {e}")

    def download_file(self, filename: str) -> Optional[BinaryIO]:
        """
        Download file from MinIO
        
        Args:
            filename: Filename in storage
            
        Returns:
            BinaryIO: File data stream or None if not found
        """
        try:
            response = self.client.get_object(self.resume_bucket, filename)
            return response
        except S3Error as e:
            if e.code == "NoSuchKey":
                return None
            raise Exception(f"Failed to download file from MinIO: {e}")

    def delete_file(self, filename: str) -> bool:
        """
        Delete file from MinIO
        
        Args:
            filename: Filename in storage
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            self.client.remove_object(self.resume_bucket, filename)
            return True
        except S3Error as e:
            print(f"Failed to delete file from MinIO: {e}")
            return False

    def get_file_url(self, filename: str, expires: int = 3600) -> str:
        """
        Get presigned URL for file download
        
        Args:
            filename: Filename in storage
            expires: URL expiration time in seconds
            
        Returns:
            str: Presigned URL
        """
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.resume_bucket,
                object_name=filename,
                expires=timedelta(seconds=expires)
            )
            return url
        except S3Error as e:
            raise Exception(f"Failed to generate presigned URL: {e}")

    def file_exists(self, filename: str) -> bool:
        """
        Check if file exists in storage
        
        Args:
            filename: Filename in storage
            
        Returns:
            bool: True if file exists
        """
        try:
            self.client.stat_object(self.resume_bucket, filename)
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            raise Exception(f"Failed to check file existence: {e}")

    def get_file_info(self, filename: str) -> Optional[dict]:
        """
        Get file information
        
        Args:
            filename: Filename in storage
            
        Returns:
            dict: File information or None if not found
        """
        try:
            stat = self.client.stat_object(self.resume_bucket, filename)
            return {
                "size": stat.size,
                "content_type": stat.content_type,
                "last_modified": stat.last_modified.isoformat() if hasattr(stat.last_modified, 'isoformat') else str(stat.last_modified),
                "etag": stat.etag
            }
        except S3Error as e:
            if e.code == "NoSuchKey":
                return None
            raise Exception(f"Failed to get file info: {e}")


# Global instance
file_storage = FileStorageService()
