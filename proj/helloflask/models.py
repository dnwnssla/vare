# coding: utf-8
from helloflask.init_db import Base
from sqlalchemy import  Column, Integer, String, Date, ForeignKey,ForeignKeyConstraint,Index
from sqlalchemy.orm import relationship, backref


class DiagDoc(Base):
    __tablename__ = 'diag_doc'
    __table_args__ = (
        ForeignKeyConstraint(['diag_id', 'pat_id'], ['diagnosis.diag_id', 'diagnosis.pat_id']),
        Index('fk_diag_doc_diagnosis1_idx', 'diag_id', 'pat_id')
    )
    pat_id = Column(Integer, primary_key=True, nullable=False)
    diag_id = Column(Integer, primary_key=True, nullable=False)
    doc_id = Column(ForeignKey('doctor.doc_id'), primary_key=True, nullable=False, index=True)
    diag_date = Column(Date, nullable=False)

    diag = relationship('Diagnosi', primaryjoin='and_(DiagDoc.diag_id == Diagnosi.diag_id, DiagDoc.pat_id == Diagnosi.pat_id)', backref='diag_docs')
    doc = relationship('Doctor', primaryjoin='DiagDoc.doc_id == Doctor.doc_id', backref='diag_docs')


class MedicalHistory(Base):
    __tablename__ = 'medical_history'
    __table_args__ = (
        ForeignKeyConstraint(['pat_id', 'diag_id', 'doc_id'], ['diag_doc.pat_id', 'diag_doc.diag_id', 'diag_doc.doc_id']),
    )
    pat_id = Column(Integer, primary_key=True, nullable=False)
    diag_id = Column(Integer, primary_key=True, nullable=False)
    doc_id = Column(String(10), primary_key=True, nullable=False)
    day = Column(Date, nullable=False)
    type = Column(String(2), nullable=False)


class Reservation(Base):
    __tablename__ = 'reservation'
    __table_args__ = (
        ForeignKeyConstraint(['pat_id', 'diag_id', 'doc_id'], ['diag_doc.pat_id', 'diag_doc.diag_id', 'diag_doc.doc_id']),
        Index('fk_reservation_diag_doc1_idx', 'pat_id', 'diag_id', 'doc_id')
    )
    pat_id = Column(Integer, primary_key=True, nullable=False)
    diag_id = Column(Integer, primary_key=True, nullable=False)
    doc_id = Column(String(10), primary_key=True, nullable=False)
    resv_date = Column(Date, nullable=False)



class Diagnosi(Base):
    __tablename__ = 'diagnosis'

    diag_id = Column(Integer, primary_key=True, nullable=False)
    pat_id = Column(ForeignKey('paitent.pat_id'), primary_key=True, nullable=False, index=True)
    diag_name = Column(String(6), nullable=False)
    diag_type = Column(String(2), nullable=False)

    pat = relationship('Paitent', primaryjoin='Diagnosi.pat_id == Paitent.pat_id', backref='diagnosis')


class HosEvalu(Base):
    __tablename__ = 'hos_evalu'

    pat_id = Column(ForeignKey('diagnosis.pat_id'), primary_key=True, index=True)



class DocEvalu(Base):
    __tablename__ = 'doc_evalu'
    __table_args__ = (
        ForeignKeyConstraint(['pat_id', 'diag_id', 'doc_id'], ['diag_doc.pat_id', 'diag_doc.diag_id', 'diag_doc.doc_id'], ondelete='CASCADE'),
    )
    pat_id = Column(Integer, primary_key=True, nullable=False)
    diag_id = Column(Integer, primary_key=True, nullable=False)
    doc_id = Column(String(10), primary_key=True, nullable=False)
    doc_evalu_itemname = Column(Integer, primary_key=True, nullable=False)
    doc_evalu_text = Column(String(45))
    doc_evalu_score = Column(Integer, nullable=False)

    pat = relationship('DiagDoc', primaryjoin='and_(DocEvalu.pat_id == DiagDoc.pat_id, DocEvalu.diag_id == DiagDoc.diag_id, DocEvalu.doc_id == DiagDoc.doc_id)', backref='doc_evalus')



class Doctor(Base):
    __tablename__ = 'doctor'

    doc_id = Column(String(10), primary_key=True)
    doc_name = Column(String(6), nullable=False)
    doc_major = Column(String(8), nullable=False)



class Paitent(Base):
    __tablename__ = 'paitent'

    pat_RRnum = Column(String(15), nullable=False)
    pat_id = Column(Integer, primary_key=True)
    pat_name = Column(String(6), nullable=False)
    pat_phonum = Column(String(19), nullable=False)
    pat_type = Column(String(2), nullable=False)
