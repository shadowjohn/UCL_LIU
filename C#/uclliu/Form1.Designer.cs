namespace uclliu
{
    partial class Form1
    {
        /// <summary>
        /// 設計工具所需的變數。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清除任何使用中的資源。
        /// </summary>
        /// <param name="disposing">如果應該處置 Managed 資源則為 true，否則為 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form 設計工具產生的程式碼

        /// <summary>
        /// 此為設計工具支援所需的方法 - 請勿使用程式碼編輯器修改
        /// 這個方法的內容。
        /// </summary>
        public void InitializeComponent()
        {
            this.output_label = new System.Windows.Forms.Label();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.word_label = new System.Windows.Forms.Label();
            this.btn_UCL = new System.Windows.Forms.Button();
            this.btn_HALF = new System.Windows.Forms.Button();
            this.btn_X = new System.Windows.Forms.Button();
            this.type_label = new System.Windows.Forms.Label();
            this.tableLayoutPanel1.SuspendLayout();
            this.SuspendLayout();
            // 
            // output_label
            // 
            this.output_label.AutoSize = true;
            this.output_label.Location = new System.Drawing.Point(12, 40);
            this.output_label.Name = "output_label";
            this.output_label.Size = new System.Drawing.Size(33, 12);
            this.output_label.TabIndex = 0;
            this.output_label.Text = "label1";
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.AutoSize = true;
            this.tableLayoutPanel1.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.tableLayoutPanel1.CellBorderStyle = System.Windows.Forms.TableLayoutPanelCellBorderStyle.Single;
            this.tableLayoutPanel1.ColumnCount = 5;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle());
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle());
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 150F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 300F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 33F));
            this.tableLayoutPanel1.Controls.Add(this.word_label, 3, 0);
            this.tableLayoutPanel1.Controls.Add(this.btn_UCL, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.btn_HALF, 1, 0);
            this.tableLayoutPanel1.Controls.Add(this.btn_X, 4, 0);
            this.tableLayoutPanel1.Controls.Add(this.type_label, 2, 0);
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel1.Margin = new System.Windows.Forms.Padding(0);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 1;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(559, 37);
            this.tableLayoutPanel1.TabIndex = 1;
            this.tableLayoutPanel1.Paint += new System.Windows.Forms.PaintEventHandler(this.tableLayoutPanel1_Paint);
            this.tableLayoutPanel1.MouseDown += new System.Windows.Forms.MouseEventHandler(this.tableLayoutPanel1_MouseDown);
            this.tableLayoutPanel1.MouseMove += new System.Windows.Forms.MouseEventHandler(this.tableLayoutPanel1_MouseMove);
            this.tableLayoutPanel1.MouseUp += new System.Windows.Forms.MouseEventHandler(this.tableLayoutPanel1_MouseUp);
            // 
            // word_label
            // 
            this.word_label.AutoSize = true;
            this.word_label.Font = new System.Drawing.Font("微軟正黑體", 18F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(136)));
            this.word_label.Location = new System.Drawing.Point(227, 1);
            this.word_label.Name = "word_label";
            this.word_label.Size = new System.Drawing.Size(0, 31);
            this.word_label.TabIndex = 5;
            // 
            // btn_UCL
            // 
            this.btn_UCL.FlatAppearance.BorderSize = 0;
            this.btn_UCL.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btn_UCL.Font = new System.Drawing.Font("微軟正黑體", 15.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(136)));
            this.btn_UCL.Location = new System.Drawing.Point(1, 1);
            this.btn_UCL.Margin = new System.Windows.Forms.Padding(0);
            this.btn_UCL.Name = "btn_UCL";
            this.btn_UCL.Size = new System.Drawing.Size(35, 35);
            this.btn_UCL.TabIndex = 1;
            this.btn_UCL.Text = "肥";
            this.btn_UCL.UseVisualStyleBackColor = true;
            this.btn_UCL.Click += new System.EventHandler(this.btn_UCL_Click);
            // 
            // btn_HALF
            // 
            this.btn_HALF.FlatAppearance.BorderSize = 0;
            this.btn_HALF.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btn_HALF.Font = new System.Drawing.Font("微軟正黑體", 15.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(136)));
            this.btn_HALF.Location = new System.Drawing.Point(37, 1);
            this.btn_HALF.Margin = new System.Windows.Forms.Padding(0);
            this.btn_HALF.Name = "btn_HALF";
            this.btn_HALF.Size = new System.Drawing.Size(35, 35);
            this.btn_HALF.TabIndex = 2;
            this.btn_HALF.Text = "半";
            this.btn_HALF.UseVisualStyleBackColor = true;
            this.btn_HALF.Click += new System.EventHandler(this.btn_HALF_Click);
            // 
            // btn_X
            // 
            this.btn_X.FlatAppearance.BorderSize = 0;
            this.btn_X.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btn_X.Font = new System.Drawing.Font("微軟正黑體", 15.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(136)));
            this.btn_X.Location = new System.Drawing.Point(525, 1);
            this.btn_X.Margin = new System.Windows.Forms.Padding(0);
            this.btn_X.Name = "btn_X";
            this.btn_X.Size = new System.Drawing.Size(32, 35);
            this.btn_X.TabIndex = 3;
            this.btn_X.Text = "╳";
            this.btn_X.UseVisualStyleBackColor = true;
            this.btn_X.Click += new System.EventHandler(this.btn_X_Click);
            // 
            // type_label
            // 
            this.type_label.AutoSize = true;
            this.type_label.Font = new System.Drawing.Font("微軟正黑體", 18F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(136)));
            this.type_label.Location = new System.Drawing.Point(76, 1);
            this.type_label.Name = "type_label";
            this.type_label.Size = new System.Drawing.Size(0, 31);
            this.type_label.TabIndex = 4;
            // 
            // Form1
            // 
            this.AccessibleRole = System.Windows.Forms.AccessibleRole.Window;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
            this.ClientSize = new System.Drawing.Size(547, 81);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Controls.Add(this.output_label);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "Form1";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.TopMost = true;
            this.Load += new System.EventHandler(this.Form1_Load);
            this.MouseDown += new System.Windows.Forms.MouseEventHandler(this.Form1_MouseDown);
            this.MouseMove += new System.Windows.Forms.MouseEventHandler(this.Form1_MouseMove);
            this.MouseUp += new System.Windows.Forms.MouseEventHandler(this.Form1_MouseUp);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        public System.Windows.Forms.Label output_label;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        public System.Windows.Forms.Button btn_X;
        public System.Windows.Forms.Button btn_UCL;
        public System.Windows.Forms.Button btn_HALF;
        public System.Windows.Forms.Label word_label;
        public System.Windows.Forms.Label type_label;
    }
}

