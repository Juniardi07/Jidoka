from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Session(models.Model):
     _name = 'jidokaacademy.session'
     _inherit = 'mail.thread'
     _description = 'jidokaacademy.session'

     name = fields.Char(string='Title', required=True, track_visibility='onchange')
     start_date = fields.Date(string='Start Date', default= fields.Date.today(), track_visibility='onchange')
     duration = fields.Float(string=' Duration', track_visibility='onchange')
     number_of_seats = fields.Float(string='Number Of Seats', track_visibility='onchange')
     description = fields.Text(string='Description', track_visibility='onchange')
     partner_id = fields.Many2one('res.partner', string='Instructor', domain="[('is_instructor','=',True)]", track_visibility='onchange')
     partner_ids = fields.Many2many('res.partner', string='Attendees', track_visibility='onchange')
     course_id = fields.Many2one('jidokaacademy.course', string='Course', required=True, track_visibility='onchange')
     taken_seats = fields.Float('taken_seats', compute='count_taken_seats', track_visibility='onchange')
     active = fields.Boolean(default=True, track_visibility='onchange')
     number_of_attendees = fields.Float('number_of_attendees', compute='count_attendees', store=True, track_visibility='onchange')

     state = fields.Selection(string='State', selection=[
          ('draft', 'Draft'),
          ('confirm', 'Confirm'),
          ('done', 'Done'),
          ('cancel', 'Cancel'),
     ], readonly=True, default='draft', required=True,)

     def action_confirm(self):
          #validasi
          #manipulasi
          self.write({'state': 'confirm'})

     def action_done(self):
          #validasi
          #manipulasi
          self.write({'state': 'done'})
     
     def action_cancel(self):
          #validasi
          #manipulasi
          self.write({'state': 'cancel'})

     def action_reset(self):
          #validasi
          #manipulasi
          self.write({'state': 'draft'})

     def unlink(self):
          if self.filtered(lambda line: line.state != 'draft'):
               raise ValidationError('Tidak bisa hapus data selain draft')
          return super(Session, self).unlink()

     @api.depends('partner_ids')
     def count_attendees(self):
          for rec in self:
               rec.number_of_attendees = len(rec.partner_ids)

     def count_taken_seats(self):
          for rec in self:
               if rec.partner_ids and rec.number_of_seats:
                    rec.taken_seats = len(rec.partner_ids) / rec.number_of_seats * 100
               else:
                    rec.taken_seats = 0

     @api.onchange('number_of_seats', 'partner_ids')
     def _onchange_number_of_seats(self):
          if self.number_of_seats < 0:
               return {
                    'warning': {
                         'title': "Invalid Value",
                         'message': "Cannot add negative number on seats"
                    }
               }
          if len(self.partner_ids) > self.number_of_seats:
               return {
                    'warning': {
                         'title': "Something bad happened",
                         'message': "Participans more than seats"
                    }
               }
          
     @api.constrains('partner_ids', 'partner_id')
     def _check_attendees(self):
          for record in self:
               if record.partner_id in record.partner_ids:
                    raise ValidationError("Instructor cannot be attendees: %s" % record.partner_id.name) 