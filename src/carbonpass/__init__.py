"""CarbonPass — local-first CBAM Communication Template engine for Taiwanese fastener SMEs.

Module 1 pipeline:
    ingestion (docs -> activity data) -> allocation (facility -> per-CN-code)
    -> rules (SEE per IR 2025/2547) -> writer (EU Communication Template .xlsx)
    -> costdelta (default-vs-actual buyer screen)

Non-negotiables (docs/10_poc_blueprint.md §2A):
    * SEE is per-product-per-YEAR (determination period = calendar year), never per-shipment.
    * Output is the producer->importer Communication Template, not the EU Registry declaration.
    * Indirect (electricity) emissions are recorded but are NOT part of the CN 7318 certificate.
    * Every figure carries a source flag (actual/default) and a per-line uncertainty.
    * The tool prepares verification; it never certifies.
"""

__version__ = "0.1.0"
