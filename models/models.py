# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

class Escuela(models.Model):
	_name = 'g.escuela'

	name = fields.Char('Escuela')
	cct =fields.Char('CCT')
	cctZona = fields.Char('CCT ZONA')
	nombreDirector = fields.Char('Director')

print("################33333222234")
class calificaciones(models.Model):
	_name = 'g.calificaciones'

	@api.multi
	@api.depends('septiembre','octubre', 'noviembreDic')
	def _compute_trimestre1(self):
		for rec in self:
			rec.trimestre1 = str((rec.septiembre + rec.octubre + rec.noviembreDic)/3)
	@api.multi
	@api.depends('enero','febrero', 'marzo')
	def _compute_trimestre2(self):
		for rec in self:
			rec.trimestre2 = str((rec.enero + rec.febrero + rec.marzo)/3)
	@api.multi
	@api.depends('abril','mayo', 'junio')
	def _compute_trimestre3(self):
		for rec in self:
			rec.trimestre3 = str((rec.abril + rec.mayo + rec.junio)/3)

	@api.multi
	@api.depends('trimestre1','trimestre2', 'trimestre3')
	def _compute_generalTrimestre(self):
		for rec in self:
			rec.generalTrimestre = str(((rec.trimestre1 + rec.trimestre2 + rec.trimestre3)/3))

	@api.multi
	def boton(self):


		filtro_alumnos = []
		lista_alumnos=self.env['g.alumnos'].search(filtro_alumnos)
		for alumno in lista_alumnos:

			filtro=[('alumno','=',alumno.id)]#es solo para un alumno como le ago para todos los alumnos en general
			boton1=self.env['g.calificaciones'].search(filtro)

			suma = 0

			for el in boton1:
				suma += el.generalTrimestre
												#suma y imprime?
				print(suma)

			print(len(boton1))
			cuantosElementos = len(boton1)
			promedio = suma / cuantosElementos
			print(promedio)
			# rec.write({'generalTrimestre':promedio})
			self.env['g.anual'].sudo().create({'alumno':alumno.id,'calificacionAnual': promedio, 'fechaAnual':datetime.now()})

	# @api.multi
	# def boton(self):

	# 	for rec in self:
	# 		filtro_alumnos = [('alumno', '=', rec.alumno.id )]
	# 		# lista_alumnos=self.env['g.alumnos'].search(filtro_alumnos)
	# 		# for alumno in lista_alumnos:

	# 		# 	filtro=[('alumno','=',alumno.id)]#es solo para un alumno como le ago para todos los alumnos en general
	# 		boton1=self.env['g.calificaciones'].search(filtro_alumnos)

	# 		suma = 0

	# 		for el in boton1:
	# 			suma += el.generalTrimestre
	# 										#suma y imprime?
	# 			print(suma)

	# 		print(len(boton1))
	# 		cuantosElementos = len(boton1)
	# 		promedio = suma / cuantosElementos
	# 		print(promedio)
	# 		# rec.write({'generalTrimestre':promedio})
	# 		rec.env['g.anual'].sudo().create({'alumno':rec.alumno.id,'calificacionAnual': promedio, 'fechaAnual':datetimex.now()})

	# def prueba(self):
	# 	for rec in self:
	# 		rec.write({'diagnostico':generalTrimestre})




	alumno = fields.Many2one('g.alumnos', string='Alumno')
	materia = fields.Many2one('g.materia', string='Materias',readonly='True')

	name = fields.Char('calificaciones')
	diagnostico = fields.Float('Diagnostico')
	septiembre = fields.Float('Septiembre')
	octubre = fields.Float('Octubre')
	noviembreDic = fields.Float('Nov/Dic')
	enero = fields.Float('Enero')
	febrero = fields.Float('Febrero')
	marzo = fields.Float('Marzo')
	abril = fields.Float('Abril')
	mayo = fields.Float('Mayo')
	junio = fields.Float('Junio')
	trimestre1 = fields.Float(compute='_compute_trimestre1', string='Trimestre 1')
	trimestre2 = fields.Float(compute='_compute_trimestre2', string='Trimestre 2')
	trimestre3 = fields.Float(compute='_compute_trimestre3', string='Trimestre 3')
	generalTrimestre = fields.Float(compute='_compute_generalTrimestre', string='Calificaacion Timeestral General')


class calificacion_Anual(models.Model):
	_name = 'g.anual'

	alumno = fields.Many2one('g.alumnos', string='alumno')
	calificacionAnual = fields.Float('Calificaciones Anuales')
	fechaAnual = fields.Date('Fecha del Año')


class alumnos(models.Model):
	_name = 'g.alumnos'

	@api.model
	def create(self, vals):
		if len (vals["name"])>20:
			raise UserError('"NOMBRE" MAYOR A 20 CARACTERES')
		if len(vals["name"])<0:
			raise UserError('"NOMBRE" NO TIENE CARACTERES')
		if len (vals["apellidoPaterno"])>20:
			raise UserError('"APELLIDO PATERNO MAYOR A 20 CARACTERES')
		if len (vals["apellidoMaterno"])>20:
			raise UserError('"APELLIDO MATERNO" MAYOR A 20 CARACTERES')
		if len(vals["edad"])>3:
			raise UserError('"EDAD" ES MAYOR A 2 CARACTERES O INTODUCISTE UNA LETRA')
		if len(vals["curp"])>16:
			raise UserError('"CURP" ES MAYOR A 16 CARACTERES')
		if len(vals["numeroTelefono"])>10:
			raise UserError('"EL NUMERO TELEFONICO" ES MAYOR A 10 CARACTERES')
		if len(vals["nombreTutor"])>30:
			raise UserError('"EL NOMBRE DEL TUTOR" ES MAYOR A 30 CARACTERES')
		return super(alumnos,self).create(vals)


	name = fields.Char('Nombre')
	apellidoPaterno = fields.Char("Apellido Paterno")
	apellidoMaterno = fields.Char('Apellido Materno')
	fechaNacimiento = fields.Date('Fecha de Nacimiento')
	sexo = fields.Selection([('M','Masculino'),('F','Femenino'),],string='Sexo')
	edad = fields.Integer('Edad')
	curp = fields.Char('curp')
	numeroTelefono = fields.Integer('Numero de Telefono')
	nombreTutor = fields.Char('Nombre del padre o tutor')
	calificaciones = fields.One2many('g.calificaciones', 'alumno', string='Calificaciones', readonly='True')
	grupo = fields.Many2one('g.grupo', string='Grupo')


class materia(models.Model):
	_name = 'g.materia'


	name = fields.Char('Materia')
	calificaciones = fields.One2many('g.calificaciones', 'materia', string='Calificaciones')
	grupo = fields.Many2one('g.grupo', string='Grupo')


class grupo(models.Model):
	_name = 'g.grupo'

	alumno = fields.One2many('g.alumnos', 'grupo', string='Alumno', readonly='True')
	materia = fields.One2many('g.materia', 'grupo', string='Materias', readonly='True')
	name = fields.Char('Grupo')
	maestros = fields.Many2one('g.maestros', string='Maestros')


class maestros(models.Model):
	_name = 'g.maestros'

	name = fields.Char('Maestro')






# class gestionboletas(models.Model):
#     _name = 'gestionboletas.gestionboletas'

#     name = fields.Char()

#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
