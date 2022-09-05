function save_and_close(fig, name)
    %function that saves a figure and closes it but makes sure it is
    %visible upon reopening
    set(fig, 'CreateFcn', 'set(gcbo,''Visible'',''on'')');     
    saveas(fig, name); close(fig);   
end