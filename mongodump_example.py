from core import MongoDump


"""
Use the parameters according to your need;
"""
mongodump = MongoDump(
    # host='<host>',
    # port=27017,
    # username='<username>',
    # password='<password>',
    # db='<db>',
    # authenticationDatabase='<authenticationDatabase>'
    )


"""
Perform dump/backup;
"""
success, backup_path = mongodump.dump()
print(success, backup_path)


"""
If you want, Compress the backup;
"""
success, compressed_backup_path = mongodump.compress_backup(
    backup_path=backup_path
)

print(success, compressed_backup_path)



# [============================ Under development ============================]


# """
# If desired, send compressed backup to google drive;
# """
# success = mongodump.send_backup_to_google_drive(
#     compressed_backup_path=compressed_backup_path
# )

# print(success)


# """
# If you want, Decompress the backup;
# """
# success, uncompressed_backup_path = mongodump.decompress_backup(
#     compressed_backup_path=compressed_backup_path
# )

# print(success, compressed_backup_path)



