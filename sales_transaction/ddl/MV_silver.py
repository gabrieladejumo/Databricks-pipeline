# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %sql
# MAGIC DECLARE silver_catalog ='dev';
# MAGIC DECLARE bronze_catalog = 'dev';
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cell 2
# MAGIC %sql
# MAGIC DROP MATERIALIZED VIEW IF EXISTS dev.silver.trasactions_enriched;
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW dev.silver.trasactions_enriched 
# MAGIC REFRESH POLICY INCREMENTAL
# MAGIC AS 
# MAGIC
# MAGIC SELECT 
# MAGIC     t.transactionID as transaction_id,
# MAGIC     t.customerID as customer_id,
# MAGIC     t.franchiseID as franchise_id,
# MAGIC     s.supplierID as supplier_id,
# MAGIC     CAST(t.quantity * t.unitPrice AS decimal(12,2)) as amount,
# MAGIC     t.paymentMethod as payment_method,
# MAGIC     CAST(t.dateTime as date) as transaction_date,
# MAGIC     t.totalPrice as total_price,
# MAGIC     T.product,
# MAGIC     COALESCE(c.first_name || ' ' || c.last_name,'Unknown') as customer_name,
# MAGIC     c.address as customer_address,
# MAGIC     c.city as customer_city,
# MAGIC     c.state as customer_state,
# MAGIC     c.postal_zip_code as customer_zipcode,  
# MAGIC     c.continent as customer_continent,
# MAGIC     c.country as customer_country,  
# MAGIC     s.name as supplier_name,  
# MAGIC     s.approved as supplier_approved,  
# MAGIC     s.continent as supplier_continent,  
# MAGIC     s.district as supplier_district,  
# MAGIC     f.name as franchise_name,  
# MAGIC     f.city as franchise_city,  
# MAGIC     f.district as franchise_district,  
# MAGIC     f.country as franchise_country  
# MAGIC   
# MAGIC FROM  dev.bronze.bronze_transactions t
# MAGIC  INNER JOIN dev.bronze.bronze_customers c   
# MAGIC  ON t.customerid = c.customerid
# MAGIC INNER JOIN dev.bronze.bronze_franchises f 
# MAGIC  ON t.franchiseid = f.franchiseid
# MAGIC  inner join dev.bronze.bronze_suppliers s
# MAGIC  ON s.supplierid = f.supplierid