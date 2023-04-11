db = db.getSiblingDB('admin');
db.createUser(
  {
    user: 'khangvt146',
    pwd: 'khang123@',
    roles: [{ role: 'readWrite', db: 'admin' }],
  },
);


db = db.getSiblingDB('amazon_crawler');
db.createUser(
  {
    user: 'khangvt146',
    pwd: 'khang123@',
    roles: [{ role: 'readWrite', db: 'amazon_best_seller' }],
  },
);
